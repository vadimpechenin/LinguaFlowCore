import {useEffect, useRef, useState} from "react"
import WordCard from "../components/WordCard";
import { getReviewWords, sendReviewAnswer } from "../api/review"
import type { RecommendWord, AnswerProgress } from "../types/review"
import { Typography, Box } from "@mui/material"

export default function ReviewPage(){

    const [words,setWords] = useState<RecommendWord[]>([])
    const [index,setIndex] = useState(0)
    const [flipped,setFlipped] = useState(false)
    const startTime = useRef<number>(0)
    const loaded = useRef(false)

    useEffect(()=>{
        if (loaded.current) return
        loaded.current = true
        loadWords()

    },[])

    const loadWords = async ()=>{

        const data = await getReviewWords()
        alert("Get words");
        setWords(data)

    }

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
        console.log("SEND", answer)
        try {

            await sendReviewAnswer(answer)

            setFlipped(false)
            setIndex(index + 1)

        } catch (err) {
            console.error(err)
        }
    }

    if (!currentWord) {
        return <div>No words for review</div>
    }

    return (
        <div>

            <h1>Review</h1>

            <WordCard
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