from RPA.Robocorp.WorkItems import WorkItems


def get_work_items_variables():
    work_items = WorkItems()
    work_items.get_input_work_item()

    return work_items.get_work_item_variables()
