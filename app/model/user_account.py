from db import insert_returning_last_id, run
import app.type.userAccount as user_account


def createUserAccount(body: user_account.CreateUserAccountBody) -> dict | None:
    sql = "INSERT INTO user_account (username, password, role) VALUES (%s, %s, %s)"
    params = [body.username, body.password, body.user_role.value]
    new_id = insert_returning_last_id(sql, params)
    return getUserAccountByID(new_id)


def getUserAccountByID(user_id: int) -> dict | None:
    sql = "SELECT * FROM user_account WHERE user_id = %s"
    params = [user_id]
    return run(sql, params, fetch="one")


def getUserAccountByUsername(username: str) -> dict | None:
    sql = "SELECT * FROM user_account WHERE username = %s"
    params = [username]
    return run(sql, params, fetch="one")


def removeUserAccountByID(user_id: int) -> dict:
    sql = "DELETE FROM user_account WHERE user_id = %s"
    params = [user_id]
    run(sql, params, commit=True)
    return {"user_id": id}


def removeUserAccountByUsername(username: str) -> dict:
    sql = "DELETE FROM user_account WHERE username = %s"
    params = [username]
    run(sql, params, commit=True)
    return {"username": username}


def listUserAccounts() -> list[dict]:
    sql = "SELECT * FROM user_account"
    params: list = []
    return run(sql, params, fetch="all")


def updateUserAccount(body: user_account.UpdateUserAccountBody) -> dict | None:
    set_parts: list[str] = []
    params: list = []
    if body.username is not None:
        set_parts.append("username = %s")
        params.append(body.username)
    if body.password is not None:
        set_parts.append("password = %s")
        params.append(body.password)
    if body.user_role is not None:
        set_parts.append("role = %s")
        params.append(body.user_role.value)
    if set_parts:
        params.append(body.user_id)
        sql = f"UPDATE user_account SET {','.join(set_parts)} WHERE user_id = %s"
        run(sql, params, commit=True)
    return getUserAccountByID(body.user_id)
