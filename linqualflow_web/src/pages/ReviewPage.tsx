import { useEffect, useRef, useState } from "react"
import { useLocation, useNavigate } from "react-router-dom"

import WordCard from "../components/WordCard"
import { getReviewWords, sendReviewAnswer } from "../api/review"

import type { RecommendWord, AnswerProgress } from "../types/review"

import { Typography, Box, Button, Table, TableBody, TableCell, TableHead, TableRow } from "@mui/material"

interface ReviewResult {
    word: RecommendWord
    correct: boolean
}

export default function ReviewPage() {
    const location = useLocation();
    const navigate = useNavigate()

    const [words, setWords] = useState<RecommendWord[]>([])
    const [index, setIndex] = useState(0)
    const [flipped, setFlipped] = useState(false)

    const [results, setResults] = useState<ReviewResult[]>([])
    const [finished, setFinished] = useState(false)

    const [loading, setLoading] = useState(true)
    const [sending, setSending] = useState(false)

    const startTime = useRef<number>(0)

    // загрузка слов
    useEffect(() => {

        const loadWords = async () => {
            try {
                // 1. Пытаемся взять слова из навигации
                const stateWords = (location.state as { words: RecommendWord[] })?.words;

                if (stateWords && stateWords.length > 0) {
                    setWords(stateWords);
                } else {
                    // 2. Если в state пусто, запрашиваем с сервера (fallback)
                    const data = await getReviewWords();
                    setWords(data);
                }
            } catch (err) {
                console.error("Ошибка загрузки слов:", err);
            } finally {
                setLoading(false);
            }
        };

        loadWords()

    }, [location.state]); // Добавляем зависимость от state

    // Loading
    if (loading) {

        return (

            <Box textAlign="center" mt={10}>
                <Typography variant="h5">
                    Loading words...
                </Typography>
            </Box>

        )

    }

    // Нет слов
    if (words.length === 0) {

        return (

            <Box textAlign="center" mt={10}>
                <Typography variant="h5">
                    No words to review 🎉
                </Typography>

                <Button
                    sx={{ mt: 3 }}
                    variant="contained"
                    onClick={() => navigate("/")}
                >
                    Back
                </Button>

            </Box>

        )

    }

    const currentWord = words[index]

    const handleFlip = () => {

        setFlipped(true)

        startTime.current = Date.now()

    }

    const handleAnswer = async (correct: boolean) => {

        if (!currentWord || sending) return

        setSending(true)

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

            if (nextIndex >= words.length) {

                setFinished(true)

            } else {

                setIndex(nextIndex)
                setFlipped(false)

            }

        } catch (err) {

            console.error(err)

        } finally {

            setSending(false)

        }

    }

    // Экран результатов
    if (finished) {

        return (

            <Box p={4}>

                <Typography variant="h4" mb={3}>
                    Review completed 🎉
                </Typography>

                <Table>

                    <TableHead>

                        <TableRow>

                            <TableCell>Word</TableCell>
                            <TableCell>Transcription</TableCell>
                            <TableCell>Translation</TableCell>
                            <TableCell>Result</TableCell>

                        </TableRow>

                    </TableHead>

                    <TableBody>

                        {results.map((r, i) => (

                            <TableRow key={i}>

                                <TableCell>{r.word.texten}</TableCell>

                                <TableCell>
                                    {r.word.transcription || "-"}
                                </TableCell>

                                <TableCell>
                                    {r.word.textl}
                                </TableCell>

                                <TableCell>
                                    {r.correct ? "✔ Correct" : "✘ Wrong"}
                                </TableCell>

                            </TableRow>

                        ))}

                    </TableBody>

                </Table>

                <Box mt={4}>

                    <Button
                        variant="contained"
                        onClick={() => navigate("/")}
                    >
                        Back to menu
                    </Button>

                </Box>

            </Box>

        )

    }

    return (

        <Box textAlign="center" mt={6}>

            <Typography variant="h4" mb={2}>
                Review
            </Typography>

            <Typography mb={3}>
                {index + 1} / {words.length}
            </Typography>

            <WordCard
                key={currentWord.id}
                word={currentWord}
                onFlip={handleFlip}
            />

            {flipped && (

                <Box mt={3} display="flex" gap={2} justifyContent="center">

                    <Button
                        variant="outlined"
                        color="error"
                        disabled={sending}
                        onClick={() => handleAnswer(false)}
                    >
                        Wrong
                    </Button>

                    <Button
                        variant="contained"
                        color="success"
                        disabled={sending}
                        onClick={() => handleAnswer(true)}
                    >
                        Correct
                    </Button>

                </Box>

            )}

        </Box>

    )

}
