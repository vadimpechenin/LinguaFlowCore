import React, { useState } from "react";
import { register } from "../api/auth";
import {backButtonStyle} from "../components/Styles";
import { useNavigate } from "react-router-dom";
import {ArrowLeft} from 'lucide-react';


export default function RegisterPage() {
    const [name,setName] = useState("");
    const [username,setUsername] = useState("");
    const [email,setEmail] = useState("");
    const [password,setPassword] = useState("");
    const [initiallevel,setInitiallevel] = useState("");
    const navigate = useNavigate()

    const handleSubmit = async (e:any) => {

        e.preventDefault();

        await register({
            name,
            username,
            email,
            password,
            initiallevel
        });

        alert("Registered");

    };

    return (

        <div>
            <button
                onClick={() => navigate('/')}
                style={backButtonStyle}
            >
                <ArrowLeft size={20} />
                {"Back to Dashboard"}
            </button>
            <h2>Register</h2>

            <form onSubmit={handleSubmit}>
                <input
                    placeholder="name"
                    value={name}
                    onChange={e => setName(e.target.value)}
                />
                <input
                    placeholder="username"
                    value={username}
                    onChange={e => setUsername(e.target.value)}
                />
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
                <input
                    placeholder="initiallevel"
                    value={initiallevel}
                    onChange={e => setInitiallevel(e.target.value)}
                />

                <button type="submit">Register</button>

            </form>

        </div>

    );

}
