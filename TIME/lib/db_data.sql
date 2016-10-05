CREATE INDEX fk_Team_idx       ON Users_In_Teams (Team_ID);
CREATE INDEX fk_nodeplugin_idx ON Node_Plugin_Info (Plugin_ID);
CREATE INDEX fk_source_idx     ON Edges (Source_ID);
CREATE INDEX fk_target_idx     ON Edges (Target_ID);
CREATE INDEX fk_Plugin_idx     ON Nodes (Plugin_ID);
CREATE INDEX fk_Case_Team_idx  ON Case_Access (Team_ID);

INSERT INTO Teams          VALUES(0, 'TIME');
INSERT INTO Users          VALUES(0, 'TIME', '$pbkdf2-sha256$8000$FwJgbI2xdq4VQg$fEvFLy7f8A1asZFM0Duw8zq1eA5joOJa.xaDz0bMScQ');
INSERT INTO Users_In_Teams VALUES(0, 0);
