import logging

from celery import shared_task

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.urls import reverse_lazy

from ..games.models import Game
from ..games.tasks import Player, run_game
from .emails import email_send
from .models import Tournament, TournamentGame, TournamentPlayer
from .utils import chunks, get_winners, make_pairings

logger = logging.getLogger("othello")


@shared_task
def run_tournament_game(tournament_game_id: int) -> str:
    try:
        t_game = TournamentGame.objects.get(id=tournament_game_id)
    except TournamentGame.DoesNotExist as e:
        logger.error(f"Trying to run a tournament game that does not exist {tournament_game_id}")
        raise e

    game = t_game.game
    run_game(game.id)
    game.refresh_from_db()
    return game.outcome


@shared_task
def run_tournament(tournament_id: int) -> None:
    try:
        t = Tournament.objects.get(id=tournament_id)
    except Tournament.DoesNotExist as e:
        logger.error(f"Trying to run tournament that does not exist {tournament_id}")
        raise e

    submissions = TournamentPlayer.objects.bulk_create(
        [TournamentPlayer(tournament=t, submission=s) for s in t.include_users.all()]
    )
    bye_player = TournamentPlayer.objects.create(tournament=t, submission=t.bye_player)

    for round_num in range(t.num_rounds):
        matches = make_pairings(submissions, bye_player)
        t.refresh_from_db()
        if t.terminated:
            t.delete()
            logger.info(f"Tournament {tournament_id} has been terminated")
            return
        t.played = round_num + 1
        t.save(update_fields=["played"])
        for round_matches in chunks(matches, settings.CONCURRENT_GAME_LIMIT):
            games = [
                t.games.create(
                    game=Game.objects.create(
                        black=game[0].submission,
                        white=game[1].submission,
                        time_limit=t.game_time_limit,
                        playing=True,
                        is_tournament=True,
                        runoff=t.runoff_enabled,
                    )
                )
                for game in round_matches
            ]
            tasks = {game: run_tournament_game.delay(game.id) for game in games}
            while len(tasks) != 0:
                finished_games = []
                for game, task in tasks.items():
                    if task.ready():
                        if task.result == Player.BLACK.value:
                            p = t.players.get(submission=game.game.black)
                            p.ranking += 1
                            p.save(update_fields=["ranking"])
                        elif task.result == Player.WHITE.value:
                            p = t.players.get(submission=game.game.white)
                            p.ranking += 1
                            p.save(update_fields=["ranking"])
                        else:
                            b, w = (
                                t.players.get(submission=game.game.black),
                                t.players.get(submission=game.game.white),
                            )
                            b.ranking += 0.5
                            w.ranking += 0.5
                            b.save(update_fields=["ranking"])
                            w.save(update_fields=["ranking"])
                        finished_games.append(game)

                for game in finished_games:
                    del tasks[game]
    t.finished = True
    t.save(update_fields=["finished"])
    logger.info(f"Tournament {tournament_id} has now finished, sending emails")

    winners = [x.submission.user for x in get_winners(submissions)]
    for pos, winner in enumerate(winners):
        email_send(
            "emails/winner.txt",
            "emails/winner.html",
            {
                "name": winner.short_name,
                "rank": "1st" if pos == 0 else "2nd" if pos == 1 else "3rd",
                "base_url": "https://othello.tjhsst.edu",
                "ranking_url": reverse_lazy("tournaments:current"),
                "dev_email": settings.DEVELOPER_EMAIL,
            },
            " Congratulations!",
            [winner.email],
        )
    email_send(
        "emails/tournament_finished.txt",
        "emails/tournament_finished.html",
        {
            "tournament_id": tournament_id,
            "start_time": t.start_time,
            "winners": [f"{x.get_full_name()} ({x.short_name})" for x in winners],
            "base_url": "https://othello.tjhsst.edu",
            "ranking_url": reverse_lazy("tournaments:current"),
            "dev_email": settings.DEVELOPER_EMAIL,
        },
        " Tournament Completed",
        [
            x.email
            for x in get_user_model().objects.filter(
                Q(is_teacher=True) | Q(is_staff=True) | Q(is_superuser=True)
            )
        ],
    )
