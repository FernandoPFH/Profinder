CREATE TABLE IF NOT EXISTS Users (
    Email text not null, 
    Password tinytext not null, 
    Type varchar(10) not null, 
    Code varchar(30) not null, 
    Name tinytext not null, 
    Image text null
    );

CREATE TABLE IF NOT EXISTS Projects (
    ProjectCode varchar(30) not null, 
    Titulo text not null,
    Descr text not null,
    Publicado tinyint(1) not null,
    Image text null
    );

CREATE TABLE IF NOT EXISTS ProjectCodexUserCode (
    ProjectCode varchar(30) not null, 
    UserCode varchar(30) not null
    );

CREATE TABLE IF NOT EXISTS ProjectCodexArea (
    ProjectCode varchar(30) not null, 
    Area tinytext not null
    );