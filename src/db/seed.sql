INSERT INTO dbo.Venue(Name, City, Address) VALUES
('Kongresové centrum', 'Praha', '5. května 1640/65'),
('Klub Orion', 'Brno', 'Uličná 12');

INSERT INTO dbo.Customer(Email, FullName, Phone) VALUES
('jana@example.com','Jana Nováková','+420111222333'),
('petr@example.com','Petr Svoboda','+420999888777');

INSERT INTO dbo.Event(VenueId, Title, StartsAt, Capacity, TicketPrice, Status)
VALUES
(1,'Tech Night', DATEADD(day,7,SYSDATETIME()), 120, 499.0, 'Published'),
(2,'Indie Live', DATEADD(day,14,SYSDATETIME()), 80, 299.0, 'Published');
