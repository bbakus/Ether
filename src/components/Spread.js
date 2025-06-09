import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import '../styles/Spread.css';
import config from '../config';

function Spread(){
    const [userQuestion, setUserQuestion] = useState('')
    const [spread, setSpread] = useState([])
    const [pulledCards, setPulledCards] = useState(0)
    const [spreadChosen, setSpreadChosen] = useState(false)
    const [spreadOrder, setSpreadOrder] = useState('')
    const [loading, setLoading] = useState(false)
    const [reading, setReading] = useState(null)
    const [autoGenerateReading, setAutoGenerateReading] = useState(false)
    const [cardsWithReversals, setCardsWithReversals] = useState([])

    function handleUserQuestion(e){
        setUserQuestion(e.target.value)
    }

    // Add random reversals to cards (30% chance each card is reversed)
    const addReversals = (cards) => {
        return cards.map(card => {
            const isReversed = Math.random() < 0.5
            console.log(`Card ${card.name}: ${isReversed ? 'REVERSED' : 'UPRIGHT'}`) // Debug log
            return {
                ...card,
                reversed: isReversed
            }
        })
    }

    // Fetch cards when pulledCards is set and greater than 0
    useEffect(() => {
        if(pulledCards > 0) {
            setLoading(true)
            // Clear existing cards first to prevent any display issues
            setSpread([])
            setCardsWithReversals([])
            
            fetch(`${config.API_URL}/cards/random/${pulledCards}`)
            .then(res => res.json())
            .then(data => {
                
                // Ensure we have unique cards
                const uniqueCards = data.filter((card, index, self) => 
                    index === self.findIndex(c => c.id === card.id)
                );
                
                if (uniqueCards.length !== data.length) {
                    console.error('Duplicate cards detected from API!', data);
                }
                
                const cardsWithReversalStatus = addReversals(uniqueCards)
                setSpread(cardsWithReversalStatus)
                setCardsWithReversals(cardsWithReversalStatus)
                setLoading(false)
            })
            .catch(error => {
                console.error('Error fetching cards:', error)
                setLoading(false)
            })
        }
    }, [pulledCards])

    // Auto-generate reading when cards are loaded (for all spreads)
    useEffect(() => {
        if (cardsWithReversals.length > 0 && !loading && !reading && spreadChosen) {
            console.log('Auto-generating reading for cards:', cardsWithReversals.map(c => `${c.name}${c.reversed ? ' (REVERSED)' : ''}`));
            
            // Calculate delay based on spread type for dramatic effect
            let delay = 1000; // Default delay
            if (spreadOrder === 'celtic-cross') {
                delay = 6000; // Wait for all 10 cards to appear (5s + 1s buffer)
            } else if (spreadOrder === 'chakra-spread') {
                delay = 4500; // Wait for all 7 cards (3.5s + 1s buffer)
            } else if (spreadOrder === 'three-card-spread') {
                delay = 2500; // Wait for all 3 cards (1.5s + 1s buffer)
            } else if (spreadOrder === 'single-card') {
                delay = 1500; // Wait for single card (0.5s + 1s buffer)
            }
            
            setTimeout(() => {
                generateAIReading()
            }, delay)
        }
        
        // Reset auto-generate flag if it was set
        if (autoGenerateReading) {
            setAutoGenerateReading(false)
        }
    }, [cardsWithReversals, loading, reading, spreadChosen, spreadOrder])

    function randomCardPull(e){
        const buttonValue = e.target.textContent;

        if(buttonValue === 'Single Card'){
            setPulledCards(1)
            setSpreadOrder('single-card')
        }else if(buttonValue === 'Three Card Spread'){
            setPulledCards(3)
            setSpreadOrder('three-card-spread')
        }else if(buttonValue === 'Celtic Cross'){
            setPulledCards(10)
            setSpreadOrder('celtic-cross')
        }else if(buttonValue === 'Chakra Spread'){
            setPulledCards(7)
            setSpreadOrder('chakra-spread')
        }

        setSpreadChosen(true)
    }

    // Generate AI reading with reversed card consideration
    const generateAIReading = async () => {
        if (cardsWithReversals.length === 0) return;
        
        setLoading(true)
        
        // Prepare cards for AI with reversal info
        const cardsForAI = cardsWithReversals.map(card => ({
            ...card,
            description: card.reversed 
                ? `${card.description} (REVERSED: This card appears upside down, which typically reverses or blocks its traditional meaning)`
                : card.description
        }))

        try {
            const response = await fetch(`${config.API_URL}/reading`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    cards: cardsForAI,
                    spread_type: spreadOrder,
                    question: userQuestion || 'General guidance'
                })
            })
            
            const data = await response.json()
            
            if (response.ok) {
                setReading(data.reading)
            } else {
                console.error('Error generating reading:', data.error)
            }
        } catch (error) {
            console.error('Error generating reading:', error)
        }
        setLoading(false)
    }

    // Quick question reading (single card)
    const handleQuestionReading = async () => {
        if (!userQuestion.trim()) return;
        
        setPulledCards(1)
        setSpreadOrder('single-card')
        setSpreadChosen(true)
        setAutoGenerateReading(true) // Flag to auto-generate when cards load
    }


    // Return to spread selection (reset everything)
    const returnToSpreadSelection = () => {
        setSpread([])
        setCardsWithReversals([])
        setReading(null)
        setSpreadChosen(false)
        setPulledCards(0)
        setSpreadOrder('')
        setUserQuestion('')
    }

    return(
        <div className="spread-container">
            <img className='spread-background' src='/images/spread-background.png' alt="Cosmic background"/>

            {spreadChosen ? (
                <div className="spread-content">
                    <div className="cards-section">
                        {loading && <div className="loading">Generating your reading...</div>}
                        
                        <div className={`cards-display ${spreadOrder}`}>
                            {spread.map(card => (
                                <div key={card.id} className={`card-item ${card.reversed ? 'reversed' : ''}`}>
                                    <img 
                                        src={`${config.API_URL}/${card.image}`} 
                                        alt={card.name}
                                    />
                                    
                                    {card.reversed && <span className="reversed-label">REVERSED</span>}
                                </div>
                            ))}
                        </div>

                        {/* Scroll indicator for chakra spread */}
                        {spreadOrder === 'chakra-spread' && spread.length > 0 && (
                            <div className="chakra-scroll-indicator">
                                <p>Scroll down to see all chakras</p>
                                <div className="scroll-arrow">↓</div>
                            </div>
                        )}



                    </div>

                    <div className="reading-section">
                        {reading && (
                            <div className="reading-result">
                                <h3>Your Cosmic Reading</h3>
                                {reading.overall_message && (
                                    <div>
                                        <h4>Overall Message</h4>
                                        <p>{reading.overall_message}</p>
                                    </div>
                                )}
                                {reading.advice && (
                                    <div>
                                        <h4>Guidance</h4>
                                        <p>{reading.advice}</p>
                                    </div>
                                )}
                                {reading.theme && (
                                    <div>
                                        <h4>Theme</h4>
                                        <p>{reading.theme}</p>
                                    </div>
                                )}
                            </div>
                        )}
                        
                        {/* Navigation button - show when cards are drawn */}
                        {spread.length > 0 && (
                            <div className="reading-actions">
                                <button 
                                    className="cosmic-button secondary"
                                    onClick={returnToSpreadSelection}
                                >
                                    ← Back to Spreads
                                </button>
                            </div>
                        )}
                    </div>
                </div>
            ) : (
                <div>
                    <input 
                        className="question-input"
                        onChange={e => handleUserQuestion(e)} 
                        placeholder='Ask a question for instant reading'
                        value={userQuestion}
                    />
                    
                    {/* Quick Question Button */}
                    {userQuestion.trim() && (
                        <button 
                            className="ai-reading-button"
                            onClick={handleQuestionReading}
                        >
                            Get Instant Reading
                        </button>
                    )}
                    
                    <div className="spread-buttons">
                        <button onClick={e => randomCardPull(e)} className='cosmic-button'>Single Card</button>
                        <button onClick={e => randomCardPull(e)} className='cosmic-button'>Three Card Spread</button>
                        <button onClick={e => randomCardPull(e)} className='cosmic-button'>Celtic Cross</button>
                        <button onClick={e => randomCardPull(e)} className='cosmic-button'>Chakra Spread</button>
                    </div>
                </div>
            )}
        </div>
    )
}

export default Spread
