from fastapi import APIRouter, HTTPException
from sqlmodel import select

from blazing.db import SessionType
from blazing.models.pokemon import Pokemon


router = APIRouter(
    prefix="/pokemon",
)

@router.post("/")
def add_pokemon(pokemon: Pokemon, session: SessionType) -> Pokemon:
    session.add(pokemon)
    session.commit()
    session.refresh(pokemon)

    return pokemon

@router.get("/{pokemon_id}")
def get_pokemon(pokemon_id: int, session: SessionType) -> Pokemon:
    pokemon = session.get(Pokemon, pokemon_id)
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    return pokemon

@router.delete("/{pokemon_id}")
def delete_pokemon(pokemon_id: int, session: SessionType):
    try:
        pokemon = get_pokemon(pokemon_id, session)
    except HTTPException:
        raise

    session.delete(pokemon)
    session.commit()
    return {"ok": True}

@router.get("/")
def list_pokemon(session: SessionType) -> list[Pokemon]:
    return list(session.exec(select(Pokemon)).all())
