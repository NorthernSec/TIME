CREATE TABLE IF NOT EXISTS Cases (
  Case_ID      SERIAL  PRIMARY KEY,
  Title        TEXT        NULL,
  Description  TEXT        NULL,
  Notes        TEXT        NULL,
  Recurse      INT     NOT NULL  DEFAULT 2);

CREATE TABLE IF NOT EXISTS Snapshots (
  SnapShot_ID    SERIAL     PRIMARY KEY,
  Case_ID        INT        NOT NULL,
  Snapshot_time  TIMESTAMP  NOT NULL DEFAULT CURRENT_TIMESTAMP,

  CONSTRAINT fk_Case
    FOREIGN KEY (Case_ID)
    REFERENCES Cases (Case_ID)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

CREATE TABLE IF NOT EXISTS Plugins (
  Plugin_ID  SERIAL  PRIMARY KEY,
  Name       TEXT    NOT NULL  UNIQUE,
  Color      TEXT    NOT NULL,
  Size       INT     NOT NULL  DEFAULT 30);

CREATE TABLE IF NOT EXISTS Intel_Types(
  Intel_ID    SERIAL  PRIMARY KEY,
  Intel_Type  TEXT    NOT NULL  UNIQUE);

CREATE TABLE IF NOT EXISTS Nodes (
  SnapShot_ID    INT    NOT NULL,
  UUID           TEXT   NOT NULL,
  Plugin_ID      INT    NOT NULL,
  Type_ID        INT    NOT NULL,
  Name           TEXT   NOT NULL,
  Label          TEXT   NOT NULL,
  Recurse_Depth  INT    NOT NULL,
  Size           INT    NOT NULL,
  Color          TEXT   NOT NULL,
  x              FLOAT      NULL,
  y              FLOAT      NULL,

  PRIMARY KEY (SnapShot_ID, UUID),
  CONSTRAINT fk_Snapshot
    FOREIGN KEY (SnapShot_ID)
    REFERENCES Snapshots (SnapShot_ID)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_Plugin
    FOREIGN KEY (Plugin_ID)
    REFERENCES Plugins (Plugin_ID)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT fk_intel_type
    FOREIGN KEY (Type_ID)
    REFERENCES Intel_Types (Intel_ID)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT);


CREATE TABLE IF NOT EXISTS Edges (
  SnapShot_ID  INT   NOT NULL,
  Source_ID    TEXT  NOT NULL,
  Target_ID    TEXT  NOT NULL,
  Label        TEXT  NOT NULL,

  PRIMARY KEY (SnapShot_ID, Source_ID, Target_ID),
  CONSTRAINT fk_source
    FOREIGN KEY (SnapShot_ID, Source_ID)
    REFERENCES Nodes (SnapShot_ID, UUID)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_target
    FOREIGN KEY (SnapShot_ID, Target_ID)
    REFERENCES Nodes (SnapShot_ID, UUID)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_ID
    FOREIGN KEY (SnapShot_ID)
    REFERENCES Snapshots (SnapShot_ID)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

CREATE TABLE IF NOT EXISTS Node_Plugin_Info (
  Snapshot_ID  Int   NOT NULL,
  Node_UUID    TEXT  NOT NULL,
  Plugin_ID    INT   NOT NULL,
  Info         TEXT      NULL,

  PRIMARY KEY (SnapShot_ID, Node_UUID, Plugin_ID),
  CONSTRAINT fk_node
    FOREIGN KEY (Snapshot_ID, Node_UUID)
    REFERENCES Nodes (Snapshot_ID, UUID)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_plugin
    FOREIGN KEY (Plugin_ID)
    REFERENCES Plugins (Plugin_ID)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT);

CREATE TABLE IF NOT EXISTS Users (
  User_ID   SERIAL  PRIMARY KEY,
  username  TEXT    NOT NULL  UNIQUE,
  hash      TEXT    NOT NULL);

CREATE TABLE IF NOT EXISTS Teams (
  Team_ID  SERIAL  PRIMARY KEY,
  Name     TEXT    NOT NULL  UNIQUE);

CREATE TABLE IF NOT EXISTS Users_In_Teams (
  User_ID INT NOT NULL,
  Team_ID INT NOT NULL,

  PRIMARY KEY (User_ID, Team_ID),
  CONSTRAINT fk_User
    FOREIGN KEY (User_ID)
    REFERENCES Users (User_ID)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_Team
    FOREIGN KEY (Team_ID)
    REFERENCES Teams (Team_ID)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

CREATE TABLE IF NOT EXISTS Case_Access (
  Case_ID INT NOT NULL,
  Team_ID INT NOT NULL,
  PRIMARY KEY (Case_ID, Team_ID),
  CONSTRAINT fk_Case
    FOREIGN KEY (Case_ID)
    REFERENCES Cases (Case_ID)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_Team
    FOREIGN KEY (Team_ID)
    REFERENCES Teams (Team_ID)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
