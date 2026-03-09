import type { RecommendWord } from "../types/review"
import { useState } from "react"

interface Props {
    word: RecommendWord
    onFlip: () => void
}

export default function WordCard({ word, onFlip }: Props) {
    const [flipped, setFlipped] = useState(false)

    const handleFlip = () => {
        setFlipped(true)
        onFlip()
    }

    return (
        <div className="card">

            {!flipped && (
                <>
                    <h2>{word.texten}</h2>
                    {word.transcription && <p>[{word.transcription}]</p>}

                    <button onClick={handleFlip}>
                        Show translation
                    </button>
                </>
            )}

            {flipped && (
                <>
                    <h2>{word.texten}</h2>
                    <h3>{word.textl}</h3>

                    {word.examplesentence && (
                        <p>{word.examplesentence}</p>
                    )}
                </>
            )}

        </div>
    )
}