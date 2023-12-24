from RPA.Robocorp.WorkItems import WorkItems, WorkItem


def get_input_work_item() -> WorkItem:
    work_items = WorkItems()
    return work_items.get_input_work_item()
