-- Create the Player table
CREATE TABLE Player (
    playerId SERIAL PRIMARY KEY,
    firstName VARCHAR(50) NOT NULL,
    lastName VARCHAR(50) NOT NULL,
    membershipStatus VARCHAR(20),
    timesPlayed INTEGER,
    points INTEGER,
    totalSpent DECIMAL(10, 2)
);

-- Create the Week table
CREATE TABLE Week (
    weekId SERIAL PRIMARY KEY,
    tableCount INTEGER,
    weekNo INTEGER
);

-- Create the Table table
CREATE TABLE "Table" (
    tableId SERIAL PRIMARY KEY,
    weekId INTEGER REFERENCES Week(weekId),
    seatCount INTEGER,
    pot DECIMAL(10, 2),
    buyIn DECIMAL(10, 2),
    tableNumber INTEGER
);

-- Create the PlayerTable table to establish many-to-many relationships
CREATE TABLE PlayerTable (
    playerId INTEGER REFERENCES Player(playerId),
    tableId INTEGER REFERENCES "Table"(tableId),
    placement INTEGER,
    seat INTEGER,
    totalBuyIn DECIMAL(10, 2),
    PRIMARY KEY (playerId, tableId)
);
