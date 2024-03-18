select * from saving;
select * from investment;
use finbot;

 update investment set response ="You can investment in \n1.Equity Mut;ual Funds\n2.Fixed input\n3.Unit Linked Insurance Plans(ULIPs)" where keyword_investment="longterm";
update investment set keyword_investment ="shortterm" where keyword_investment="shorterm"
 
 create table budget(id int primary key , keyword_budget  varchar(300) not null , response varchar(500));
INSERT INTO budget (id, keyword_budget)
VALUES (1 ,'food');
INSERT INTO budget (id, keyword_budget)
VALUES (2 ,'utilities');
INSERT INTO budget (id, keyword_budget)
VALUES (3 ,'tutionfees');
INSERT INTO budget (id, keyword_budget)
VALUES (4 ,'entertainment');
INSERT INTO budget (id, keyword_budget)
VALUES (5 ,'personalactivities');

create table emergency(id int primary key , keyword_emergency varchar(300) not null , response varchar(500));
INSERT INTO emergency (id, keyword_emergency)
VALUES (1 ,'emergency');