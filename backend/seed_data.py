#!/usr/bin/env python3
"""Seed the database with sample lab data for testing."""

import asyncio
import asyncpg
import os

# Use 'postgres' as host when running inside Docker container
DB_HOST = os.environ.get("POSTGRES_HOST", "postgres")
DB_PORT = int(os.environ.get("POSTGRES_PORT", "5432"))
DB_NAME = os.environ.get("POSTGRES_DB", "db-lab-8")
DB_USER = os.environ.get("POSTGRES_USER", "postgres")
DB_PASS = os.environ.get("POSTGRES_PASSWORD", "postgres")


async def seed():
    conn = await asyncpg.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
    )

    # Clear existing data
    await conn.execute("DELETE FROM interacts")
    await conn.execute("DELETE FROM item")
    await conn.execute("DELETE FROM learner")

    # Insert labs
    labs = [
        (1, "lab", "Lab 1: Introduction to Python", None),
        (2, "lab", "Lab 2: Data Structures", None),
        (3, "lab", "Lab 3: Algorithms", None),
        (4, "lab", "Lab 4: Web Development", None),
        (5, "lab", "Lab 5: Database Design", None),
        (6, "lab", "Lab 6: API Development", None),
        (7, "lab", "Lab 7: Telegram Bot", None),
        (8, "lab", "Lab 8: AI Agent", None),
    ]

    for lab_id, lab_type, name, parent_id in labs:
        await conn.execute(
            "INSERT INTO item (id, type, parent_id, name) VALUES ($1, $2, $3, $4)",
            lab_id, lab_type, parent_id, name,
        )

    # Insert tasks for Lab 1
    tasks_lab1 = [
        (101, "task", "Task 1.1: Hello World", 1),
        (102, "task", "Task 1.2: Variables", 1),
        (103, "task", "Task 1.3: Functions", 1),
    ]

    for task_id, task_type, name, parent_id in tasks_lab1:
        await conn.execute(
            "INSERT INTO item (id, type, parent_id, name) VALUES ($1, $2, $3, $4)",
            task_id, task_type, parent_id, name,
        )

    # Insert learners
    learners = [
        (1, "student1", "Student One"),
        (2, "student2", "Student Two"),
        (3, "student3", "Student Three"),
    ]

    for learner_id, username, name in learners:
        await conn.execute(
            "INSERT INTO learner (id, username, name) VALUES ($1, $2, $3)",
            learner_id, username, name,
        )

    # Insert some interactions (submissions)
    interactions = [
        (1, 1, 101, 100, "passed"),
        (2, 1, 102, 80, "passed"),
        (3, 2, 101, 90, "passed"),
        (4, 2, 102, 75, "failed"),
        (5, 3, 101, 95, "passed"),
    ]

    for int_id, learner_id, item_id, score, status in interactions:
        await conn.execute(
            "INSERT INTO interacts (id, learner_id, item_id, score, status) VALUES ($1, $2, $3, $4, $5)",
            int_id, learner_id, item_id, score, status,
        )

    await conn.close()
    print("Database seeded successfully!")
    print(f"Inserted {len(labs)} labs, {len(tasks_lab1)} tasks, {len(learners)} learners, {len(interactions)} interactions")


if __name__ == "__main__":
    asyncio.run(seed())
