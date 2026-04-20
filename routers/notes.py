from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
from database import get_db
import schemas
from Oauth2 import get_current_user, get_current_admin

router = APIRouter(prefix="/notes", tags=["Notes"])

@router.post("/", response_model= schemas.NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    new_note = models.Note(**note.dict(), owner_id=current_user.id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return [new_note]
@router.get("/", response_model= list[schemas.NoteResponse])
def get_all_notes(db: Session = Depends(get_db), 
                  current_user: models.User = Depends(get_current_user),
                  skip: int = 0, 
                  limit: int = 10):
    notes = db.query(models.Note).filter(models.Note.owner_id == current_user.id).offset(skip).limit(limit).all()
    return notes
@router.get("/get_all", response_model=list[schemas.NoteResponse])
def get_all_notes_endpoint(db: Session = Depends(get_db), 
                           current_user: models.User = Depends(get_current_admin),
                           skip: int = 0, 
                           limit: int = 10):
    notes = db.query(models.Note).offset(skip).limit(limit).all()
    return notes
@router.get("/{note_id}", response_model=schemas.NoteResponse)
def get_note_by_id(note_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.owner_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Note with id {note_id} not found")
    if note.owner_id != current_user.id and current_user.is_admin == False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to access this note")
    return note
@router.put("/{note_id}", response_model=schemas.NoteResponse)
def update_note(note_id: int, note_update: schemas.NoteUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.owner_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Note with id {note_id} not found")
    if note.owner_id != current_user.id and current_user.is_admin == False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to update this note")
    for key, value in note_update.dict(exclude_unset=True).items():
        setattr(note, key, value)
    db.commit()
    db.refresh(note)
    return note
@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.owner_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Note with id {note_id} not found")
    if note.owner_id != current_user.id and current_user.is_admin == False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to delete this note")
    db.delete(note)
    db.commit()
    return None

