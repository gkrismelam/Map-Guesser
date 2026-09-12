from drafter import *
from dataclasses import dataclass
import random
import math

@dataclass
class State:
    guess: MapMarker
    map: Map
    randMap: Map
    score: int
    round: int
    difficulty: str

@route
def index(state: State) -> Page:
    return Page(state, [
        Row(
            Header("Location"),
            Header("Guess"),
            style_justify_content="center",
            style_gap="500px"
        ),
        Row(
            Map(
                state.randMap.name,
                state.randMap.center,
                state.randMap.zoom),
            Map(
                state.map.name,
                center=(state.map.center),
                zoom=state.map.zoom,
                markers=[state.guess],
                on_click="guess",
                on_move="changeMap"),
            style_gap="10px"
        ),
        Row(
            Button("Ocean", "newMap"),
            Button("Guess!", "inputGuess"),
            SelectBox("choice", ["easy", "normal", "hard"], state.difficulty),
            Button("Change Difficulty", "changeDifficulty"),
            style_justify_content="center"
            ),
        Row(
            Header("Round " + str(state.round)),
            Header("Score " + str(state.score)),
            style_justify_content="center",
            style_gap="25px"
        )
        ])

@route
def guess(state: State, latitude: float, longitude: float) -> Page:
    state.guess = MapMarker(latitude, longitude, "Guess")
    return index(state)

@route
def changeMap(state: State, latitude: float, longitude: float, zoom: int) -> Page:
    state.map.center = MapLocation(latitude, longitude)
    state.map.zoom = zoom
    return index(state)

@route
def inputGuess(state: State) -> Page:
    distanceLatitude = (state.guess.latitude - state.randMap.center.latitude) ** 2
    distanceLongitude = (state.guess.longitude - state.randMap.center.longitude) ** 2

    distance = round(math.sqrt(distanceLatitude + distanceLongitude))
    points = max(0, round(1000 - distance * 10))
    
    state.score += points


    if state.round == 5:
        return end(state)
    
    state.round += 1
    return newMap(state)

@route
def newMap(state: State) -> Page:
    state.randMap.center = MapLocation(random.uniform(-60, 70), random.uniform(-180, 180))
    return index(state)

@route
def end(state: State) -> Page:
    return Page(state, [
        Row(
            Header("Game Finished"),
            style_justify_content="center",
        ),
        Row(
            Header("Final Score: " + str(state.score)),
            style_justify_content="center",
        )
    ])

@route
def changeDifficulty(state: State, choice: str) -> Page:
    state.difficulty = choice
    if state.difficulty == "easy":
        state.randMap.zoom = 5
    elif state.difficulty == "normal":
        state.randMap.zoom = 7
    elif state.difficulty == "hard":
        state.randMap.zoom = 10
    return index(state)


start_server(State(MapMarker(0, 0, "Guess"), Map("Map", (0, 0), 3), Map("RandMap", MapLocation(random.uniform(-60, 70), random.uniform(-180, 180)), 7), 0, 1, "normal"))
