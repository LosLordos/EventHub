IF OBJECT_ID('dbo.v_event_attendance') IS NOT NULL DROP VIEW dbo.v_event_attendance;
IF OBJECT_ID('dbo.v_event_revenue')    IS NOT NULL DROP VIEW dbo.v_event_revenue;

IF OBJECT_ID('dbo.Payment')           IS NOT NULL DROP TABLE dbo.Payment;
IF OBJECT_ID('dbo.EventParticipant')  IS NOT NULL DROP TABLE dbo.EventParticipant;
IF OBJECT_ID('dbo.TicketOrder')       IS NOT NULL DROP TABLE dbo.TicketOrder;
IF OBJECT_ID('dbo.Event')             IS NOT NULL DROP TABLE dbo.Event;
IF OBJECT_ID('dbo.Customer')          IS NOT NULL DROP TABLE dbo.Customer;
IF OBJECT_ID('dbo.Venue')             IS NOT NULL DROP TABLE dbo.Venue;

CREATE TABLE dbo.Venue (
    VenueId        INT IDENTITY(1,1) PRIMARY KEY,
    Name           VARCHAR(120) NOT NULL,
    City           VARCHAR(80)  NOT NULL,
    Address        VARCHAR(160) NOT NULL,
    IsActive       BIT NOT NULL CONSTRAINT DF_Venue_IsActive DEFAULT(1)
);

CREATE TABLE dbo.Customer (
    CustomerId     INT IDENTITY(1,1) PRIMARY KEY,
    Email          VARCHAR(140) NOT NULL UNIQUE,
    FullName       VARCHAR(140) NOT NULL,
    Phone          VARCHAR(30)  NULL,
    IsActive       BIT NOT NULL CONSTRAINT DF_Customer_IsActive DEFAULT(1),
    CreatedAt      DATETIME2 NOT NULL CONSTRAINT DF_Customer_CreatedAt DEFAULT(SYSDATETIME())
);

CREATE TABLE dbo.Event (
    EventId        INT IDENTITY(1,1) PRIMARY KEY,
    VenueId        INT NOT NULL,
    Title          VARCHAR(160) NOT NULL,
    StartsAt       DATETIME2 NOT NULL,
    Capacity       INT NOT NULL CHECK (Capacity >= 0),
    SoldCount      INT NOT NULL CONSTRAINT DF_Event_SoldCount DEFAULT(0),
    TicketPrice    FLOAT NOT NULL CHECK (TicketPrice >= 0),
    Status         VARCHAR(20) NOT NULL CHECK (Status IN ('Draft','Published','Cancelled','Finished')),
    CreatedAt      DATETIME2 NOT NULL CONSTRAINT DF_Event_CreatedAt DEFAULT(SYSDATETIME()),
    CONSTRAINT FK_Event_Venue FOREIGN KEY (VenueId) REFERENCES dbo.Venue(VenueId),
    CONSTRAINT CK_Event_Sold_Lte_Capacity CHECK (SoldCount <= Capacity)
);

CREATE TABLE dbo.TicketOrder (
    TicketOrderId  INT IDENTITY(1,1) PRIMARY KEY,
    EventId        INT NOT NULL,
    CustomerId     INT NOT NULL,
    Quantity       INT NOT NULL CHECK (Quantity > 0),
    UnitPrice      FLOAT NOT NULL CHECK (UnitPrice >= 0),
    TotalPrice     AS (Quantity * UnitPrice) PERSISTED,
    Status         VARCHAR(20) NOT NULL CHECK (Status IN ('Created','Paid','Cancelled')),
    CreatedAt      DATETIME2 NOT NULL CONSTRAINT DF_TicketOrder_CreatedAt DEFAULT(SYSDATETIME()),
    CONSTRAINT FK_TicketOrder_Event FOREIGN KEY (EventId) REFERENCES dbo.Event(EventId),
    CONSTRAINT FK_TicketOrder_Customer FOREIGN KEY (CustomerId) REFERENCES dbo.Customer(CustomerId)
);

CREATE TABLE dbo.EventParticipant (
    EventId        INT NOT NULL,
    CustomerId     INT NOT NULL,
    JoinedAt       DATETIME2 NOT NULL CONSTRAINT DF_EventParticipant_JoinedAt DEFAULT(SYSDATETIME()),
    PRIMARY KEY (EventId, CustomerId),
    CONSTRAINT FK_EventParticipant_Event FOREIGN KEY (EventId) REFERENCES dbo.Event(EventId),
    CONSTRAINT FK_EventParticipant_Customer FOREIGN KEY (CustomerId) REFERENCES dbo.Customer(CustomerId)
);

CREATE TABLE dbo.Payment (
    PaymentId      INT IDENTITY(1,1) PRIMARY KEY,
    TicketOrderId  INT NOT NULL,
    Amount         FLOAT NOT NULL CHECK (Amount >= 0),
    Method         VARCHAR(20) NOT NULL CHECK (Method IN ('Card','Cash','BankTransfer')),
    PaidAt         DATETIME2 NOT NULL CONSTRAINT DF_Payment_PaidAt DEFAULT(SYSDATETIME()),
    IsRefund       BIT NOT NULL CONSTRAINT DF_Payment_IsRefund DEFAULT(0),
    CONSTRAINT FK_Payment_TicketOrder FOREIGN KEY (TicketOrderId) REFERENCES dbo.TicketOrder(TicketOrderId)
);

CREATE VIEW dbo.v_event_attendance AS
SELECT
    e.EventId,
    e.Title,
    e.StartsAt,
    e.Capacity,
    e.SoldCount,
    Remaining = (e.Capacity - e.SoldCount)
FROM dbo.Event e;

CREATE VIEW dbo.v_event_revenue AS
SELECT
    e.EventId,
    e.Title,
    Revenue = SUM(CASE WHEN p.IsRefund = 0 THEN p.Amount ELSE -p.Amount END),
    PaymentsCount = COUNT(p.PaymentId)
FROM dbo.Event e
JOIN dbo.TicketOrder o
