button::before {
    content: "";
    position: absolute;
    display: block;
    top: 0;
    left: -50px;
    width: 150%;
    height: 100%;
    background: $14202d;
    transition: all 0.7s ease-in-out;
    z-index: -1;
    transform: translateX(-300px) skew(.20deg);
}

button:hover::before{
    transform: translateX(0px) skew(-20deg);
}