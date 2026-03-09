import {useEffect, useRef, useState} from "react"
import { useNavigate } from "react-router-dom"
import WordCard from "../components/WordCard";
import { getReviewWords, sendReviewAnswer } from "../api/review"
import type { RecommendWord, AnswerProgress } from "../types/review"
import { Typography, Box } from "@mui/material"


interface ReviewResult {
    word: RecommendWord
    correct: boolean
}

export default function ReviewPage(){

    const navigate = useNavigate()

    const [words,setWords] = useState<RecommendWord[]>([])
    const [index,setIndex] = useState(0)
    const [flipped,setFlipped] = useState(false)

    const [results, setResults] = useState<ReviewResult[]>([])
    const [finished, setFinished] = useState(false)

    const startTime = useRef<number>(0)
    const loaded = useRef(false)

    useEffect(()=>{
        if (loaded.current) return
        loaded.current = true

        const loadWords = async ()=>{
            const data = await getReviewWords()
            setWords(data)
        }
        loadWords()
    },[])

    if(words.length === 0){

        return(

            <Box textAlign="center" mt={10}>
                <Typography variant="h5">
                    No words to review 🎉
                </Typography>
            </Box>

        )

    }

    const currentWord = words[index]

    const handleFlip = () => {
        setFlipped(true)
        startTime.current = Date.now()
    }


    const handleAnswer = async (correct: boolean) => {

        if (!currentWord) return

        const responseTime = Date.now() - startTime.current

        const answer: AnswerProgress = {
            wordid: currentWord.id,
            iscorrect: correct,
            response_time_ms: responseTime
        }

        try {

            await sendReviewAnswer(answer)

            setResults(prev => [
                ...prev,
                { word: currentWord, correct }
            ])

            const nextIndex = index + 1
            //alert(nextIndex)
            if (nextIndex >= words.length) {
                setFinished(true)
            } else {
                //alert("Попал в следующий")
                setIndex(nextIndex)
                setFlipped(false)
            }

        } catch (err) {
            console.error(err)
        }
    }


    if (words.length === 0) {
        return <div>Loading...</div>
    }


    if (finished) {
        return (
            <div>

                <h1>Review completed</h1>

                <table border={1} cellPadding={8}>
                    <thead>
                    <tr>
                        <th>Word</th>
                        <th>Transcription</th>
                        <th>Translation</th>
                        <th>Result</th>
                    </tr>
                    </thead>

                    <tbody>

                    {results.map((r, i) => (
                        <tr key={i}>

                            <td>{r.word.texten}</td>

                            <td>
                                {r.word.transcription || "-"}
                            </td>

                            <td>{r.word.textl}</td>

                            <td>
                                {r.correct ? "✔ Correct" : "✘ Wrong"}
                            </td>

                        </tr>
                    ))}

                    </tbody>
                </table>

                <br/>

                <button onClick={() => navigate("/")}>
                    Back to menu
                </button>

            </div>
        )
    }


    if (!currentWord) {
        return <div>No words</div>
    }


    return (
        <div>

            <h1>Review</h1>

            <p>
                {index + 1} / {words.length}
            </p>

            <WordCard
                key={currentWord.id}
                word={currentWord}
                onFlip={handleFlip}
            />

            {flipped && (

                <div style={{ marginTop: 20 }}>

                    <button
                        onClick={() => handleAnswer(false)}
                    >
                        Wrong
                    </button>

                    <button
                        onClick={() => handleAnswer(true)}
                    >
                        Correct
                    </button>

                </div>

            )}

        </div>
    )
}
