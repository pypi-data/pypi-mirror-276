from typing import List
from uuid import UUID

import orjson
from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile, status
from sqlalchemy import or_, update
from sqlmodel import Session, select

from langflow.api.v1.flows import create_flows
from langflow.api.v1.schemas import FlowListCreate, FlowListReadWithFolderName
from langflow.services.auth.utils import get_current_active_user
from langflow.services.database.models.flow.model import Flow, FlowCreate, FlowRead
from langflow.services.database.models.folder.constants import DEFAULT_FOLDER_NAME
from langflow.services.database.models.folder.model import (
    Folder,
    FolderCreate,
    FolderRead,
    FolderReadWithFlows,
    FolderUpdate,
)
from langflow.services.database.models.user.model import User
from langflow.services.deps import get_session

router = APIRouter(prefix="/folders", tags=["Folders"])


@router.post("/", response_model=FolderRead, status_code=201)
def create_folder(
    *,
    session: Session = Depends(get_session),
    folder: FolderCreate,
    current_user: User = Depends(get_current_active_user),
):
    try:
        new_folder = Folder.model_validate(folder, from_attributes=True)
        new_folder.user_id = current_user.id

        folder_results = session.exec(
            select(Folder).where(
                Folder.name.like(f"{new_folder.name}%"),  # type: ignore
                Folder.user_id == current_user.id,
            )
        )
        existing_folder_names = [folder.name for folder in folder_results]

        if existing_folder_names:
            new_folder.name = f"{new_folder.name} ({len(existing_folder_names) + 1})"

        session.add(new_folder)
        session.commit()
        session.refresh(new_folder)

        if folder.components_list:
            update_statement_components = (
                update(Flow).where(Flow.id.in_(folder.components_list)).values(folder_id=new_folder.id)  # type: ignore
            )
            session.exec(update_statement_components)  # type: ignore
            session.commit()

        if folder.flows_list:
            update_statement_flows = update(Flow).where(Flow.id.in_(folder.flows_list)).values(folder_id=new_folder.id)  # type: ignore
            session.exec(update_statement_flows)  # type: ignore
            session.commit()

        return new_folder
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[FolderRead], status_code=200)
def read_folders(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
):
    try:
        folders = session.exec(
            select(Folder).where(
                or_(Folder.user_id == current_user.id, Folder.user_id == None)  # type: ignore # noqa: E711
            )
        ).all()
        return folders
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{folder_id}", response_model=FolderReadWithFlows, status_code=200)
def read_folder(
    *,
    session: Session = Depends(get_session),
    folder_id: UUID,
    current_user: User = Depends(get_current_active_user),
):
    try:
        folder = session.exec(select(Folder).where(Folder.id == folder_id, Folder.user_id == current_user.id)).first()
        if not folder:
            raise HTTPException(status_code=404, detail="Folder not found")
        return folder
    except Exception as e:
        if "No result found" in str(e):
            raise HTTPException(status_code=404, detail="Folder not found")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{folder_id}", response_model=FolderRead, status_code=200)
def update_folder(
    *,
    session: Session = Depends(get_session),
    folder_id: UUID,
    folder: FolderUpdate,  # Assuming FolderUpdate is a Pydantic model defining updatable fields
    current_user: User = Depends(get_current_active_user),
):
    try:
        existing_folder = session.exec(
            select(Folder).where(Folder.id == folder_id, Folder.user_id == current_user.id)
        ).first()
        if not existing_folder:
            raise HTTPException(status_code=404, detail="Folder not found")
        folder_data = folder.model_dump(exclude_unset=True)
        for key, value in folder_data.items():
            if key != "components" and key != "flows":
                setattr(existing_folder, key, value)
        session.add(existing_folder)
        session.commit()
        session.refresh(existing_folder)

        concat_folder_components = folder.components + folder.flows

        flows_ids = session.exec(select(Flow.id).where(Flow.folder_id == existing_folder.id)).all()

        excluded_flows = list(set(flows_ids) - set(concat_folder_components))

        my_collection_folder = session.exec(select(Folder).where(Folder.name == DEFAULT_FOLDER_NAME)).first()
        if my_collection_folder:
            update_statement_my_collection = (
                update(Flow).where(Flow.id.in_(excluded_flows)).values(folder_id=my_collection_folder.id)  # type: ignore
            )
            session.exec(update_statement_my_collection)  # type: ignore
            session.commit()

        if concat_folder_components:
            update_statement_components = (
                update(Flow).where(Flow.id.in_(concat_folder_components)).values(folder_id=existing_folder.id)  # type: ignore
            )
            session.exec(update_statement_components)  # type: ignore
            session.commit()

        return existing_folder

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{folder_id}", status_code=204)
def delete_folder(
    *,
    session: Session = Depends(get_session),
    folder_id: UUID,
    current_user: User = Depends(get_current_active_user),
):
    try:
        folder = session.exec(select(Folder).where(Folder.id == folder_id, Folder.user_id == current_user.id)).first()
        if not folder:
            raise HTTPException(status_code=404, detail="Folder not found")
        session.delete(folder)
        session.commit()
        flows = session.exec(select(Flow).where(Flow.folder_id == folder_id, Folder.user_id == current_user.id)).all()
        for flow in flows:
            session.delete(flow)
        session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/{folder_id}", response_model=FlowListReadWithFolderName, status_code=200)
async def download_file(
    *,
    session: Session = Depends(get_session),
    folder_id: UUID,
    current_user: User = Depends(get_current_active_user),
):
    """Download all flows from folder."""
    try:
        folder = session.exec(select(Folder).where(Folder.id == folder_id, Folder.user_id == current_user.id)).first()
        return folder
    except Exception as e:
        if "No result found" in str(e):
            raise HTTPException(status_code=404, detail="Folder not found")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload/", response_model=List[FlowRead], status_code=201)
async def upload_file(
    *,
    session: Session = Depends(get_session),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
):
    """Upload flows from a file."""
    contents = await file.read()
    data = orjson.loads(contents)

    if not data:
        raise HTTPException(status_code=400, detail="No flows found in the file")

    folder_results = session.exec(
        select(Folder).where(
            Folder.name == data["folder_name"],
            Folder.user_id == current_user.id,
        )
    )
    existing_folder_names = [folder.name for folder in folder_results]

    if existing_folder_names:
        data["folder_name"] = f"{data['folder_name']} ({len(existing_folder_names) + 1})"

    folder = FolderCreate(name=data["folder_name"], description=data["folder_description"])

    new_folder = Folder.model_validate(folder, from_attributes=True)
    new_folder.id = None
    new_folder.user_id = current_user.id
    session.add(new_folder)
    session.commit()
    session.refresh(new_folder)

    del data["folder_name"]
    del data["folder_description"]

    if "flows" in data:
        flow_list = FlowListCreate(flows=[FlowCreate(**flow) for flow in data["flows"]])
    else:
        raise HTTPException(status_code=400, detail="No flows found in the data")
    # Now we set the user_id for all flows
    for flow in flow_list.flows:
        flow.user_id = current_user.id
        flow.folder_id = new_folder.id

    return create_flows(session=session, flow_list=flow_list, current_user=current_user)
