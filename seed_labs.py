#!/usr/bin/env python3
"""Seed the LMS database with sample lab data."""

import asyncio
import os
from sqlmodel import SQLModel, create_engine, Session, select
from app.models.item import ItemRecord

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@postgres:5432/db-lab-8")

def seed_labs():
    """Create sample labs in the database."""
    engine = create_engine(DATABASE_URL)
    
    with Session(engine) as session:
        # Check if labs already exist
        existing = session.exec(select(ItemRecord)).all()
        if existing:
            print(f"Database already has {len(existing)} items. Skipping seed.")
            return
        
        # Create labs (lab-01 through lab-10)
        labs = []
        for i in range(1, 11):
            lab = ItemRecord(
                type="lab",
                title=f"Lab {i:02d}",
                description=f"Lab {i:02d} - Software Engineering Toolkit"
            )
            session.add(lab)
            labs.append(lab)
        
        session.commit()
        
        # Refresh to get IDs
        for lab in labs:
            session.refresh(lab)
        
        # Create tasks for each lab
        for i, lab in enumerate(labs, 1):
            for task_num in range(1, 5):
                task = ItemRecord(
                    type="task",
                    parent_id=lab.id,
                    title=f"Lab {i:02d} Task {task_num}",
                    description=f"Task {task_num} for Lab {i:02d}"
                )
                session.add(task)
        
        session.commit()
        print(f"Successfully seeded {len(labs)} labs with tasks.")

if __name__ == "__main__":
    seed_labs()
