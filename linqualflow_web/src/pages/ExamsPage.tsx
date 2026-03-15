import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"

import { getUserExams, startExam } from "../api/exams"

import type { ExamResponseAllFields } from "../types/exams"

export default function ExamsPage(){

    const navigate = useNavigate()

    const [exams,setExams] = useState<ExamResponseAllFields[]>([])
    const [loading,setLoading] = useState(true)

    useEffect(()=>{

        const load = async ()=>{

            const data = await getUserExams()

            setExams(data)

            setLoading(false)

        }

        load()

    },[])

    const handleStart = async ()=>{

        const exam = await startExam({
            difficultylevel: "B2",
            size: 10
        })

        navigate("/exam-runner",{
            state: exam
        })

    }

    if(loading) return <div>Loading exams...</div>

    return(

        <div>

            <h1>Exams</h1>

            <button onClick={handleStart}>
                Start new exam
            </button>

            <h2>Your previous exams</h2>

            <table border={1} cellPadding={8}>

                <thead>

                <tr>
                    <th>Date</th>
                    <th>Level</th>
                    <th>Size</th>
                </tr>

                </thead>

                <tbody>

                {exams.map(e=>(
                    <tr key={e.id}>

                        <td>{new Date(e.takenat).toLocaleString()}</td>

                        <td>{e.difficultylevel}</td>

                        <td>{e.size}</td>

                    </tr>
                ))}

                </tbody>

            </table>

        </div>

    )

}
