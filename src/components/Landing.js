import { useNavigate } from 'react-router-dom';
import '../styles/landing.css'

function Landing(){
    const navigate = useNavigate();

    const handleEnter = () => {
        navigate('/home');
    };

    return(
        <div>
            <div className='landing-image'>
                <img src='/images/landing.png' alt="Ether Landing"/>
            </div>
            <h1 className='landing-title'>Welcome to Ether</h1>
            <button className='enter-button' onClick={handleEnter}>ENTER</button>
        </div>
    )
}

export default Landing
