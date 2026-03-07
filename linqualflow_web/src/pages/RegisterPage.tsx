import { useState } from "react";
import { register } from "../api/auth";

export default function RegisterPage() {

    const [email,setEmail] = useState("");
    const [password,setPassword] = useState("");

    const handleSubmit = async (e:any) => {

        e.preventDefault();

        await register({
            email,
            password
        });

        alert("Registered");

    };

    return (

        <div>

            <h2>Register</h2>

            <form onSubmit={handleSubmit}>

                <input
                    placeholder="email"
                    value={email}
                    onChange={e => setEmail(e.target.value)}
                />

                <input
                    type="password"
                    placeholder="password"
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                />

                <button type="submit">Register</button>

            </form>

        </div>

    );

}
