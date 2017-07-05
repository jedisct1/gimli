#include "stm32wrapper.h"

void clock_setup(void)
{
    rcc_clock_setup_in_hsi_out_48mhz();
    rcc_periph_clock_enable(RCC_GPIOA);
    rcc_periph_clock_enable(RCC_USART2);
    rcc_periph_clock_enable(RCC_DMA);
}

void gpio_setup(void)
{
    gpio_mode_setup(GPIOA, GPIO_MODE_AF, GPIO_PUPD_NONE, GPIO2 | GPIO3);
    gpio_set_af(GPIOA, GPIO_AF1, GPIO2 | GPIO3);
}

void usart_setup(int baud)
{
    usart_set_baudrate(USART2, baud);
    usart_set_databits(USART2, 8);
    usart_set_stopbits(USART2, USART_CR2_STOP_1_0BIT);
    usart_set_mode(USART2, USART_MODE_TX_RX);
    usart_set_parity(USART2, USART_PARITY_NONE);
    usart_set_flow_control(USART2, USART_FLOWCONTROL_NONE);

    usart_enable(USART2);
}

void send_USART_str(const char* in)
{
    int i;
    for(i = 0; in[i] != 0; i++) {
        usart_send_blocking(USART2, in[i]);
    }
    usart_send_blocking(USART2, '\r');
    usart_send_blocking(USART2, '\n');
}

void send_USART_bytes(const unsigned char* in, int n)
{
    int i;
    for(i = 0; i < n; i++) {
        usart_send_blocking(USART2, in[i]);
    }
}

void recv_USART_bytes(unsigned char* out, int n)
{
    int i;
    for(i = 0; i < n; i++) {
        out[i] = usart_recv_blocking(USART2);
    }
}

// for the STM32F0, interrupts for DMA_CH4 and DMA_CH5 are combined
void dma1_channel4_5_isr(void) {
    usart_disable_tx_dma(USART2);
    usart_disable_rx_dma(USART2);
    dma_clear_interrupt_flags(DMA1, DMA_CHANNEL4, DMA_TCIF);
    dma_clear_interrupt_flags(DMA1, DMA_CHANNEL5, DMA_TCIF);
    dma_disable_channel(DMA1, DMA_CHANNEL4);
    dma_disable_channel(DMA1, DMA_CHANNEL5);
}