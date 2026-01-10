lfc database

CREATE TABLE public.users
(
    id varchar(50) PRIMARY KEY,
	name varchar(50),
    username varchar(50),
	password varchar(50),
	email varchar(50),
	initiallevel varchar(2),
	createdat TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
	lastloginat TIMESTAMP WITH TIME ZONE,
	isactive BOOLEAN NOT NULL DEFAULT true
);
  
INSERT INTO users (
	id , name, username, password, email, initiallevel) 
	VALUES ('b83618b2915447688156f1106b7be703',	'Кузьма', 'administrator', 'administrator', 'kyz@mail.ru', 'B1');
	
CREATE TABLE public.usersettings
(
	userid varchar(50),
	interfacelanguage VARCHAR(10) NOT NULL DEFAULT 'ru',
	learninglanguage VARCHAR(10) NOT NULL DEFAULT 'en',
	preferredvoice VARCHAR(50),
	dailywordlimit INTEGER NOT NULL DEFAULT 20,
	enableaudio BOOLEAN NOT NULL DEFAULT true,
	enablenotifications BOOLEAN NOT NULL DEFAULT true,
	timezone VARCHAR(50) NOT NULL DEFAULT 'UTC'
);


CREATE TABLE public.words
(
    id varchar(50) PRIMARY KEY,
	texten varchar(100),
	transcription varchar(100),
	textl varchar(100),
	partOfSpeech varchar(50),
	examplesentence varchar(500),
	difficultylevel varchar(2),
	audiourl varchar(500),
	createdat TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

CREATE TABLE public.userwordprogress
(
    id varchar(50) PRIMARY KEY,
	userid varchar(50),
	wordid varchar(50),
	lastreviewed TIMESTAMP WITH TIME ZONE,
	nextreviewed TIMESTAMP WITH TIME ZONE,
	successrate REAL NOT NULL DEFAULT 0.0,
	reviewcount INTEGER NOT NULL DEFAULT 0,
	isknown BOOLEAN NOT NULL DEFAULT false,
	createdat TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

CREATE TABLE wordreviews (
    id varchar(50) PRIMARY KEY,
	userid varchar(50),
	wordid varchar(50),
    reviewedat TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    iscorrect BOOLEAN NOT NULL,
    responsetimems INTEGER
);

CREATE TABLE public.texts
(
    id varchar(50) PRIMARY KEY,
	userid varchar(50),
	title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
	language VARCHAR(10) NOT NULL DEFAULT 'en',
    createdat TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- ---------- TEXT VOCABULARY STATS ----------
CREATE TABLE public.textvocabularystats (
    id varchar(50) PRIMARY KEY,
    textid varchar(50) NOT NULL,
    totalwords INTEGER NOT NULL,
    knownwords INTEGER NOT NULL,
    unknownwords INTEGER NOT NULL,
    coveragepercent REAL NOT NULL,
    computedat TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- ---------- EXAMS ----------
CREATE TABLE public.exams (
    id varchar(50) PRIMARY KEY,
	userid varchar(50),
    title VARCHAR(255) NOT NULL,
    difficultylevel VARCHAR(2),
    score REAL,
    takenat TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- ---------- ML WORD FEATURES (OPTIONAL) ----------
CREATE TABLE public.mlwordfeatures (
    wordid varchar(50) PRIMARY KEY,
    frequencyrank INTEGER,
    avgsuccessrate REAL,
    avgreviewinterval REAL
);