UPDATE users
SET password=MD5(Password)


UPDATE users
SET password=MD5(Password)
WHERE username!='Administrator';

UPDATE users
SET password=MD5('Administrator')
WHERE username='Administrator';