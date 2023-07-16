from datetime import datetime
import random
from models import db, Episode, Guest, Appearance
from app import app

# List of guest names and occupations
guest_names = [
    "John Doe",
    "Jane Smith",
    "Michael Johnson",
    "Emily Davis",
    "David Wilson",
    # Add more names as needed
]

guest_occupations = [
    "Actor",
    "Musician",
    "Writer",
    "Comedian",
    "Athlete",
    # Add more occupations as needed
]

def seed_data():
    with app.app_context():
        # Create episodes
        episodes = []
        for i in range(1, 16):
            date_str = f'2023-01-{str(i).zfill(2)}'
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            episode = Episode(date=date_obj, number=i)
            episodes.append(episode)
        
        # Create guests
        guests = []
        for i in range(1, 16):
            name = random.choice(guest_names)
            occupation = random.choice(guest_occupations)
            guest = Guest(name=name, occupation=occupation)
            guests.append(guest)
        
        # Create appearances
        appearances = []
        for i in range(1, 16):
            appearance = Appearance(rating=i % 5 + 1, episode=episodes[i-1], guest=guests[i-1])
            appearances.append(appearance)
        
        # Add objects to session and commit changes
        db.session.add_all(episodes + guests + appearances)
        db.session.commit()

if __name__ == '__main__':
    seed_data()
