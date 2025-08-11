module de2i150_io_test(
    input  [17:0] SW,     // slide switches
    input  [3:0]  KEY,    // push-buttons (ativo-baixo)
    output [17:0] LEDR,   // LEDs vermelhos
    output [8:0]  LEDG    // LEDs verdes
);
    assign LEDR = SW;          // cada switch acende seu LEDR
    assign LEDG[3:0] = ~KEY;   // cada botão acende seu LEDG ao pressionar
    assign LEDG[8:4] = 5'b0;   // verdes restantes apagados (ou use SW[8:4] se quiser)
endmodule