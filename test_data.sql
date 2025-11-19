
-- This file can be used to generate users into the database for testing
-- You can check the passwords below. There are plain text comments next to the hash.

--NORMAL USERS
INSERT INTO users(username, password, is_admin) VALUES (
    'Veera',
    'pbkdf2:sha256:600000$pUQnosbl5lBWqUEb$3fddfa145352c7d90913e7ff2f1da80a2fed49613d1f0dc08adb0284626de77f', --Salasana
    0
);

INSERT INTO users(username, password, is_admin) VALUES (
    'Laura',
    'pbkdf2:sha256:600000$bCP1TYS0Y8znp6qP$5955b6624f8e41f41ed9a5c8d3be2717242e3bcb7c9f2fc3b9950eee0af30e42', --PossuKainalo
    0
);

INSERT INTO users(username, password, is_admin) VALUES (
    'Janne',
    'pbkdf2:sha256:600000$dRuX5rtQWJlqHeDX$5aa4456f440c7e5473d42dcc75d2916477268a7afb595ac0202528742cd1af52', --Janne123
    0
);

INSERT INTO users(username, password, is_admin) VALUES (
    'Jonne',
    'pbkdf2:sha256:600000$Qe2eLObenfHIJGBq$c46b08a6dedb7ac79fa9c8850e5e6a6b5662d5a6c7368b4263ee98ac8489d8a4', --420
    0
);

INSERT INTO users(username, password, is_admin) VALUES (
    'TestaUwU',
    'pbkdf2:sha256:600000$6STbiFUdEUugSDr4$d955a6ba454fe0531c679429e8cdbf375f90f4262fd1b4c275a14626a51d9c62', --Kawai
    0
);

INSERT INTO users(username, password, is_admin) VALUES (
    'Miguel',
    'pbkdf2:sha256:600000$gZRGohghr0dJk9nv$09aa20299120ee26e6beb9d946ec3ce009cd57d4c494297b93a3f89a8b9ade13', --Maailma
    0
);

INSERT INTO users(username, password, is_admin) VALUES (
    'Sluupiduu',
    'pbkdf2:sha256:600000$bvws6N1TXxV709DQ$49263e88bd3c35a772452e7aad7bae5939732dbd96e1ae11d10a8fda745a7e2d', --Whoopiepie
    0
);

INSERT INTO users(username, password, is_admin) VALUES (
    'Lyhyt',
    'pbkdf2:sha256:600000$iFvZFMF77e82hTVu$70bbda00769418d1df42631aa31bc3359d4b4275f01001b60b45612db9b1ecfe', --Pitkä
    0
);

INSERT INTO users(username, password, is_admin) VALUES (
    'Tunnus',
    'pbkdf2:sha256:600000$Uzo1VNZkBEdd1V3C$4cc940aa4227a85087007fb3e7a729ec73c570d5939a0333394fa160ba538c55', --Eikä ole
    0
);

INSERT INTO users(username, password, is_admin) VALUES (
    'Light mode',
    'pbkdf2:sha256:600000$InwGlatYUsFJLdhT$513c0aed26ca5dd88fb371379eff3d838b76ced5c6532da1abc7ca7f160357e4', --Bugs see light
    0
);

INSERT INTO users(username, password, is_admin) VALUES (
    'asdf',
    'pbkdf2:sha256:600000$DT7gm9BcmlHNyxC0$7e08bb2f80f4cc8c7c7f4059097b2db8f6603aa9e4c134dc8a0b5668f8d66e97', --asdf
    0
);

INSERT INTO users(username, password, is_admin) VALUES (
    'qwer',
    'pbkdf2:sha256:600000$kE9eQNBm6QHeWjxT$234cb6ee19a7e222a144afc4d06b24bbd336696954cfbaae89704a7267bc75e6', --qwer
    0
);

INSERT INTO users(username, password, is_admin) VALUES (
    'qwerty',
    'pbkdf2:sha256:600000$Oqf7GvhXDr4RjcuY$2e1984a8da267c99b2d1d71e166fd53618d5be0e5371966232c24b6252f558f5', --qwerty
    0
);

INSERT INTO users(username, password, is_admin) VALUES (
    'xyz',
    'pbkdf2:sha256:600000$Z757rS0VYZRR1Qft$c8a4f9dec6a5a5cd3f9c37e317b5e99c0a3e51936084f2fed3101ce08598156e', --xyz
    0
);

INSERT INTO users(username, password, is_admin) VALUES (
    'Syntax',
    'pbkdf2:sha256:600000$3vaqPSNQD829uasp$7468b1a64f05a1dea7d1af843bc97bec25288244f00c56f18bbecaee436634fe', --Error
    0
);






--ADMIN USERS
INSERT INTO users(username, password, is_admin) VALUES (
    'Dark mode',
    'pbkdf2:sha256:600000$gv3nIEXLTdxMjEQy$37a3484fc9c44708fe6ba5303e6a6ffaa19c5ea6dbe33acec378ca6266f2d70d', --Perfect code
    1
);

INSERT INTO users(username, password, is_admin) VALUES (
    'Esko',
    'pbkdf2:sha256:600000$G0F9sv308PDyjlx5$51a80427db319567292b970b1459b7c7bf7565fe4d1c90451b946af7474ffab7', --ToDeLlA VaHvA SaLaSaNa0!?
    1
);

INSERT INTO users(username, password, is_admin) VALUES (
    'Aq',
    'pbkdf2:sha256:600000$LJWGeHLpl0FwAr4j$f8af23dc71186cae5837dae390646ac902cc429ada1d09d36cde25e206c7e2fa', --BlenderRender
    1
);



--EXAMS
INSERT INTO exams(examname, start_key, active, exercises, points) VALUES (
    'Testikoe',
    'teStiAvain',
    1,
    '{"Kerro elämästä", "Mitä on kuolema", "Kuka ja mitä", "Missä on alku", "Kuka sinä olet"}',
    '{10,5,15,23,2}'
);

INSERT INTO exams(examname, start_key, active, exercises, points) VALUES (
    'MA12001',
    'AvainMa1122',
    0,
    '{"Laske 1+1", "Arvioi neljöjuuri 2 10 desimaalin tarkkuudella", "Laske 5/10", "Todista induktiolla x^2+a", "Oma nimesi"}',
    '{1,50,5,34,22}'
);

INSERT INTO exams(examname, start_key, active, exercises, points) VALUES (
    'TKT10001',
    'ekaKoeTKT',
    0,
    '{"Testi"}',
    '{1}'
);


INSERT INTO exams(examname, start_key, active, exercises, points) VALUES (
    'TKT20202',
    'hankalaKala',
    1,
    '{"takaperin", "edes päin", "ympäri ämpäri"}',
    '{1,2,3}'
);