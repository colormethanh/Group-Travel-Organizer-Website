### GroupTravelOrganizerWebsite
A django based website for organizing a group trip. Users can...
- Create Trips to invite friends to so that all trip information is readily avalible
- Submit events to vote on to be added to the trip, so that everyone has a say in planning the trip
- Chat within each Trip page so for further ease of planning
- Post Pictures of the trip so that everyone can easily download them

## Inspiration
As a person who loves to travel, especially with friends, I've noticed that as the trips get bigger and more ambitious people often get lost in all the planning and logistics that go into trip planning. Furthermore, different people have different levels of desired involvments for trip planning. My father would rather be told the day off where he needs to drive whereas my mother wants to know every detail about a trip. My application will seek to appease both of these groups of people. Minimizing planning and maximizing fun! 

## Models
- Trip (many to one)
- Event (many to one)
- Going (through for many to many b/w Trip and User)
- Photos (many to one)
- Voted (through for many to many b/w Event and User)
- Comment (many to one)
- Like (many to one)
