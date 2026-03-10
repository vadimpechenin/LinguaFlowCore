import { useState, useContext } from "react";
import { login } from "../api/auth";
import { AuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router-dom"

export default function LoginPage() {

    const { loginUser } = useContext(AuthContext);

    const [username, setUsername] = useState("test_user_");
    const [password, setPassword] = useState("password123");

    const navigate = useNavigate()

    const handleSubmit = async (e:any) => {

        e.preventDefault();

        try{

            const res = await login({
                username,
                password
            })

            const token = res.data.access_token

            loginUser(token)

            navigate("/")

        }catch(err){

            alert("Login failed")

        }

    };

    return (

        <div>

            <h2>Login</h2>

            <form onSubmit={handleSubmit}>

                <input
                    placeholder="username"
                    value={username}
                    onChange={e => setUsername(e.target.value)}
                />

                <input
                    type="password"
                    placeholder="password"
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                />

                <button type="submit">Войти</button>

            </form>
            <button onClick={() => navigate('/register')}>
                Зарегистрироваться
            </button>
        </div>

    );

}
