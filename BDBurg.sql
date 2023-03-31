set quoted_identifier on
go
set ansi_nulls on
go

create database Burger
go

use Burger
go
---------------
create table [Burgers]
(
	[ID_Burgers] [int] not null identity(1,1) primary key,
	[Cost_Burgers] [int] not null
)
go

insert into Burgers ([Cost_Burgers]) values
(100)
go
------------------
create table [Admin]
(
	[ID_Admin] [int] not null identity(1,1) primary key,
	[Email_Admin] [VARCHAR] (100) not null unique check ([Email_Admin] like ('%@%.%')),
	[Password_Admin] [VARCHAR] (10) not null,
	[Balance_Admin] [int] not null default(10000)
)
go

insert into [Admin] ([Email_Admin], [Password_Admin], [Balance_Admin]) values
('maxxam0302@gmail.com', '12345', 10000)
go
-----------------------
create table [Type_Ingridient]
(
	[ID_Type] [int] not null identity(1,1) primary key,
	[Name_Type] [VARCHAR] (50) not null unique
)
go

insert into [Type_Ingridient] ([Name_Type]) values
('Булка'),
('Сыр'),
('Капуста'),
('Мясо'),
('Лук'),
('Огурцы'),
('Бекон')
go
----------------------
create table [Card_Loyality]
(
	[ID_Loyality] [int] not null identity(1,1) primary key,
	[Name_Loyality] [VARCHAR] (50) not null unique,
	[Discount] [float] not null
)
go

insert into [Card_Loyality] ([Name_Loyality], [Discount]) values
('None', 0),
('Bronze', 0.10),
('Silver', 0.20),
('Gold', 0.30)
go
-------------------------
create table [User]
(
	[ID_User] [int] not null identity(1,1) primary key,
	[Loyality_ID] [int] not null references [Card_Loyality] (ID_Loyality) on delete cascade,
	[Email_User] [VARCHAR](100) not null unique check ([Email_User] like ('%@%.%')),
	[Password_User] [VARCHAR](10) not null,
	[Balance_User] [int] not null default(10000)
)
go

insert into [User] ([Loyality_ID], [Email_User], [Password_User], [Balance_User]) values
(1, 'lvatahvlatp@gmail.com', '12345', 10000)
go
-----------------------
create table [Ingridient]
(
	[ID_Ingridient] [int] not null identity(1,1) primary key,
	[Type_ID] [int] not null references [Type_Ingridient] (ID_Type) on delete cascade,
	[Name_Ingridient] [VARCHAR](50) not null unique,
	[Cost_Ingridient] [int] not null,
	[Count_Ingridient] [int] not null default(100)
)
go

insert into [Ingridient] ([Type_ID], [Name_Ingridient], [Cost_Ingridient], [Count_Ingridient]) values
(1, 'Ржанные булки', 20, 100),
(1, 'Cтандартные булки', 10, 100),
(2, 'Сыр Масдам', 40, 100),
(2, 'Сыр Чеддер', 35, 100),
(3, 'Русская капуста', 30, 100),
(3, 'Китайская капуста', 40, 100),
(4, 'Говядина', 100, 100),
(4, 'Свинина', 100, 100),
(5, 'Белый лук', 15, 100),
(5, 'Красный лук', 20, 100),
(6, 'Свежие огурцы', 10, 100),
(6, 'Соленые огурцы', 25, 100),
(7, 'Бекон сырой', 40, 100),
(7, 'Бекон жареный', 70, 100)
go
-------------------
create table [Supply]
(
	[ID_Supply] [int] not null identity(1,1) primary key,
	[Admin_ID] [int] not null references [Admin] (ID_Admin) on delete cascade,
	[Ingridient_ID] [int] not null references [Ingridient] (ID_Ingridient) on delete cascade,
	[Count_Supply] [int] not null,
	[Cost_Supply] [int] not null,
	[Sum_Supply] [int] not null
)
go

insert into [Supply] ([Admin_ID], [Ingridient_ID], [Count_Supply], [Cost_Supply], [Sum_Supply]) values
(1, 1, 20, 20, 400)
go
-------------------------
create table [Carbonara_Ingridient]
(
	[ID_Burgers_Ingridient] [int] not null identity(1,1) primary key,
	[Burgers_ID] [int] not null references [Burgers] (ID_Burgers) on delete cascade,
	[Ingridient_ID] [int] not null references [Ingridient] (ID_Ingridient) on delete cascade
)
go

insert into [Carbonara_Ingridient] ([Burgers_ID], [Ingridient_ID]) values
(1, 1),
(1, 3),
(1, 5),
(1, 7),
(1, 9),
(1, 11),
(1, 13)
go
-------------
create table [Check]
(
	[ID_Check] [int] not null identity(1,1) primary key,
	[User_ID] [int] not null references [User] (ID_User) on delete cascade,
	[Count_Burgers] [int] not null,
	[Cost_Burgers] [int] not null,
	[Sum_Order] [int] not null,
	[Time_Order] [datetime] not null,
	[Ear] [bit] not null,
	[Noticed] [bit] not null
)
go

insert into [Check] ([User_ID], [Count_Burgers], [Cost_Burgers], [Sum_Order], [Time_Order], [Ear], [Noticed]) values
(1, 1, 900, 290, SYSDATETIME(), 0, 0)
go
----------------------------
create table [Check_Burgers]
(
	[ID_Check_Burgers] [int] not null identity(1,1) primary key,
	[Check_ID] [int] not null references [Check] (ID_Check) on delete cascade,
	[Burgers_Check_ID] [int] not null references [Burgers] (ID_Burgers) on delete cascade
)
go

insert into [Check_Burgers] ([Check_ID], [Burgers_Check_ID]) values
(1,1)
go