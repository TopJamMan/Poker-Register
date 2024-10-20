-- Create the Player table
CREATE TABLE Player (
    stundertNumber VARCHAR(9) PRIMARY KEY ,
    firstName VARCHAR(50) NOT NULL,
    lastName VARCHAR(50) NOT NULL,
    membershipStatus BOOLEAN,
    timesPlayed INTEGER,
    points INTEGER,
    totalSpent DECIMAL(10, 2)
);

-- Create the Week table
CREATE TABLE Week (
    weekNo INTEGER PRIMARY KEY,
    tableCount INTEGER,

);

-- Create the Table table
CREATE TABLE game_table (
    tableId SERIAL PRIMARY KEY,
    weekNo INTEGER REFERENCES Week(weekNo),
    seatCount INTEGER,
    pot DECIMAL(10, 2),
    buyIn DECIMAL(10, 2),
    tableNumber INTEGER
);

-- Create the PlayerTable table to establish many-to-many relationships
CREATE TABLE PlayerTable (
    studentNumber INTEGER REFERENCES Player(studentNumber),
    tableId INTEGER REFERENCES Table(tableId),
    placement INTEGER,
    seat INTEGER,
    totalBuyIn DECIMAL(10, 2),
    PRIMARY KEY (studentNumber, tableId)
);
