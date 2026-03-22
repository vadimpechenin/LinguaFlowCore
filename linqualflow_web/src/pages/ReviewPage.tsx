import { useEffect, useRef, useState } from "react"
import { useLocation, useNavigate } from "react-router-dom"
import WordCard from "../components/WordCard"
import { getReviewWords, sendReviewAnswer } from "../api/review"
import type { RecommendWord, AnswerProgress } from "../types/review"
import {
    Typography, Box, Button, Table, TableBody,
    TableCell, TableHead, TableRow, Paper
} from "@mui/material"

interface ReviewResult {
    word: RecommendWord
    correct: boolean
}

// Добавляем типы для стадий страницы
type ReviewStage = 'list' | 'cards' | 'results';

export default function ReviewPage() {
    const location = useLocation();
    const navigate = useNavigate();
    // Получаем данные из state один раз при инициализации
    const stateData = location.state as { words: RecommendWord[], showList?: boolean };

    const [words, setWords] = useState<RecommendWord[]>([]);
    // Определяем начальную стадию: если showList истинно — 'list', иначе — 'cards'
    const [stage, setStage] = useState<ReviewStage>(
        stateData?.showList ? 'list' : 'cards'
    );
    const [index, setIndex] = useState(0);
    const [flipped, setFlipped] = useState(false);
    const [results, setResults] = useState<ReviewResult[]>([]);

    const [loading, setLoading] = useState(true);
    const [sending, setSending] = useState(false);
    const startTime = useRef<number>(0);

    useEffect(() => {
        const loadWords = async () => {
            try {
                const stateWords = (location.state as { words: RecommendWord[] })?.words;
                if (stateWords && stateWords.length > 0) {
                    setWords(stateWords);
                } else {
                    const data = await getReviewWords();
                    setWords(data);
                    // Если зашли по прямой ссылке (без стейта), лучше показать список
                    setStage('list');
                }
            } catch (err) {
                console.error("Ошибка загрузки слов:", err);
            } finally {
                setLoading(false);
            }
        };
        loadWords();
    }, [location.state]);

    if (loading) return <Box textAlign="center" mt={10}><Typography variant="h5">Loading...</Typography></Box>;
    if (words.length === 0) return <Box textAlign="center" mt={10}><Typography variant="h5">No words 🎉</Typography><Button sx={{ mt: 3 }} variant="contained" onClick={() => navigate("/")}>Back</Button></Box>;

    const handleAnswer = async (correct: boolean) => {
        if (sending) return;
        setSending(true);
        const responseTime = Date.now() - startTime.current;

        try {
            await sendReviewAnswer({
                wordid: words[index].id,
                iscorrect: correct,
                response_time_ms: responseTime
            });

            setResults(prev => [...prev, { word: words[index], correct }]);

            if (index + 1 >= words.length) {
                setStage('results');
            } else {
                setIndex(index + 1);
                setFlipped(false);
            }
        } catch (err) {
            console.error(err);
        } finally {
            setSending(false);
        }
    };
    // 1. ЭКРАН СПИСКА СЛОВ
    if (stage === 'list') {
        return (
            <Box p={4} maxWidth="800px" margin="0 auto">
                <Typography variant="h4" mb={3}>Words for Review</Typography>
                <Paper elevation={3}>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell>Word</TableCell>
                                <TableCell>Translation</TableCell>
                                <TableCell>Transcription</TableCell>
                                <TableCell>Level</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {words.map((w) => (
                                <TableRow key={w.id}>
                                    <TableCell sx={{ fontWeight: 'bold' }}>{w.texten}</TableCell>
                                    <TableCell>{w.textl}</TableCell>
                                    <TableCell>{w.transcription}</TableCell>
                                    <TableCell>{w.difficultylevel}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </Paper>
                <Box mt={4} display="flex" justifyContent="space-between">
                    <Button variant="outlined" onClick={() => navigate("/")}>Cancel</Button>
                    <Button
                        variant="contained"
                        size="large"
                        onClick={() => setStage('cards')}
                    >
                        Start Training
                    </Button>
                </Box>
            </Box>
        );
    }

    // Экран результатов
    if (stage === 'results') {

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
                        Back to dashboard
                    </Button>

                </Box>

            </Box>

        )

    }

    // 3. ЭКРАН КАРТОЧЕК
    const currentWord = words[index];
    return (
        <Box textAlign="center" mt={6}>
            <Typography variant="h4" mb={2}>Review</Typography>
            <Typography mb={3}>{index + 1} / {words.length}</Typography>
            <WordCard
                key={currentWord.id}
                word={currentWord}
                onFlip={() => { setFlipped(true); startTime.current = Date.now(); }}
            />
            {flipped && (
                <Box mt={3} display="flex" gap={2} justifyContent="center">
                    <Button variant="outlined" color="error" disabled={sending} onClick={() => handleAnswer(false)}>Wrong</Button>
                    <Button variant="contained" color="success" disabled={sending} onClick={() => handleAnswer(true)}>Correct</Button>
                </Box>
            )}
        </Box>

    )

}
