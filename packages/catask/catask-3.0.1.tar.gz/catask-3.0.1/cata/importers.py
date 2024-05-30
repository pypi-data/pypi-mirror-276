"""Module that provides methods to import data from other programs"""

import logging

from cata.data import *
from cata.calendars import convert_to_persian_date


class Importer:
    """Import tasks and events from files of other programs"""

    def __init__(self, user_tasks, user_events, cf):
        self.user_tasks = user_tasks
        self.user_events = user_events
        self.tasks_file = cf.TASKS_FILE
        self.events_file = cf.EVENTS_FILE
        self.use_persian_calendar = cf.USE_PERSIAN_CALENDAR

    def read_file(self, filename):
        """Try to read a file and return its lines"""
        try:
            with open(filename, "r", encoding="utf-8") as file:
                lines = file.readlines()
            return lines
        except (IOError, FileNotFoundError, NameError):
            logging.error("Problem occurred accessing %s.", filename)
            return []

    def import_tasks_from_taskwarrior(self):
        """Import tasks from taskwarrior database via taskw library"""
        from taskw import TaskWarrior

        tasks = TaskWarrior().load_tasks()
        for task in tasks["pending"]:
            name = task["description"]
            if not self.user_tasks.item_exists(name):
                task_id = self.user_tasks.generate_id()
                is_private = False
                timer = Timer([])
                status = Status.NORMAL
                self.user_tasks.add_item(Task(task_id, name, status, timer, is_private))
