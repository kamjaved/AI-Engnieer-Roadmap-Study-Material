import uuid

from fastapi import APIRouter, HTTPException, status

from fast_api_traversy.schemas import IssueCreate, IssueResponse, IssueUpdate
from fast_api_traversy.storage import load_data, save_data

router = APIRouter(prefix="/api/v1/issues", tags=["Issues"])


@router.get("", response_model=list[IssueResponse])
async def get_issues():
    """Retrive all issues."""
    issues = load_data()
    return issues


@router.post("", response_model=IssueResponse, status_code=status.HTTP_201_CREATED)
async def create_issues(payload: IssueCreate):
    """Create a  New Issue"""
    issues = load_data()
    new_issue = {
        "id": str(uuid.uuid4()),
        "title": payload.title,
        "description": payload.description,
        "priority": payload.priority,
        "state": payload.state,
    }
    issues.append(new_issue)
    save_data(issues)

    return new_issue


@router.get("/{issue_id}", response_model=IssueResponse)
async def get_issue(issue_id: str):
    """Get single issue by ID Raises 404 if issue not found"""

    issues = load_data()
    for item in issues:
        if item["id"] == issue_id:
            return item

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")


##NOTE: ----OLD FASHIONED WAY----

# @router.put("/{issue_id}", response_model=IssueResponse)
# async def update_issue(issue_id: str, payload: IssueUpdate):
#     issues = load_data()
#     for item in issues:
#         if item["id"] == issue_id:
#             if payload.title is not None:
#                 item["title"] = payload.title
#             if payload.description is not None:
#                 item["description"] = payload.description
#             if payload.priority is not None:
#                 item["priority"] = payload.priority.value
#             if payload.state is not None:
#                 item["state"] = payload.state.value

#             save_data(issues)
#             return item
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not Found")


##NOTE: ----NEW WAY INSTEAD OF CHECK EACH FIELD WITH "is Not None" we can use "model_dump(exclude_unset=True" ----


@router.put("/{issue_id}", response_model=IssueResponse)
async def update_issue(issue_id: str, payload: IssueUpdate):
    issues = load_data()
    for item in issues:
        if item["id"] == issue_id:
            item.update(payload.model_dump(exclude_unset=True, mode="json"))
            save_data(issues)
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not Found")


@router.delete("/{issue_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_issue(issue_id: str):
    issues = load_data()
    for i, item in enumerate(issues):
        if item["id"] == issue_id:
            issues.pop(i)
            save_data(issues)
            return

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not Found")
