from sqlalchemy import event
from sqlalchemy.orm import (
    ORMExecuteState,
    Session,
    with_loader_criteria,
)


@event.listens_for(Session, 'do_orm_execute')
def add_soft_delete_filter(execute_state: ORMExecuteState):
    if (
        execute_state.is_select
        and not execute_state.execution_options.get('skip_filter', False)
        and execute_state.bind_mapper is not None
        and hasattr(execute_state.bind_mapper.class_, 'deleted_at')
    ):
        cls = execute_state.bind_mapper.class_
        execute_state.statement = execute_state.statement.options(
            with_loader_criteria(
                cls,
                lambda cls_: cls_.deleted_at.is_(None),
                include_aliases=True,
            )
        )
