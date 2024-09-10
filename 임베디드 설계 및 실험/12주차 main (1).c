#include "stm32f10x.h"
#include "core_cm3.h"
#include "misc.h"
#include "stm32f10x_gpio.h"
#include "stm32f10x_rcc.h"
#include "stm32f10x_usart.h"
#include "stm32f10x_adc.h"
#include "lcd.h"
#include "touch.h"
#include <stdio.h>
#include <stdlib.h>

volatile uint32_t jodo[1];

void RCC_Configure(void);
void GPIO_Configure(void);
void ADC_Configure(void);
void DMA_Configure(void);

//---------------------------------------------------------------------------------------------------

void RCC_Configure(void)
{
  // TODO: Enable the APB2 peripheral clock using the function 'RCC_APB2PeriphClockCmd'
  RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB,ENABLE);   // RCC GPIO A
  RCC_AHBPeriphClockCmd(RCC_AHBPeriph_DMA1, ENABLE);   // DMA
  RCC_APB2PeriphClockCmd(RCC_APB2Periph_ADC1, ENABLE);    // ADC1
}

void GPIO_Configure(void)
{
   GPIO_InitTypeDef GPIO_InitStructure;

  // TODO: Initialize the GPIO pins using the structure 'GPIO_InitTypeDef' and the function 'GPIO_Init'
  GPIO_InitStructure.GPIO_Pin = GPIO_Pin_0;
  GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AIN;
  GPIO_Init(GPIOB, &GPIO_InitStructure);
}

void ADC_Configure(void) {
   ADC_InitTypeDef ADC_InitStructure;
   ADC_DeInit(ADC1);
   ADC_InitStructure.ADC_Mode = ADC_Mode_Independent;
   ADC_InitStructure.ADC_ScanConvMode = DISABLE;
   ADC_InitStructure.ADC_ContinuousConvMode = ENABLE;
   ADC_InitStructure.ADC_ExternalTrigConv = ADC_ExternalTrigConv_None;
   ADC_InitStructure.ADC_DataAlign = ADC_DataAlign_Right;
   ADC_InitStructure.ADC_NbrOfChannel = 1;
   ADC_RegularChannelConfig(ADC1, ADC_Channel_8, 1, ADC_SampleTime_239Cycles5);
   ADC_Init(ADC1, &ADC_InitStructure);
   
   ADC_DMACmd(ADC1, ENABLE);
   ADC_Cmd(ADC1, ENABLE);
   
   ADC_ResetCalibration(ADC1);
   while(ADC_GetResetCalibrationStatus(ADC1));
   ADC_StartCalibration(ADC1);
   while(ADC_GetCalibrationStatus(ADC1));
   ADC_SoftwareStartConvCmd(ADC1, ENABLE);
}

void DMA_Configure(void) {
  DMA_InitTypeDef DMA_InitStructure;
  DMA_DeInit(DMA1_Channel1);
  DMA_InitStructure.DMA_PeripheralBaseAddr = (uint32_t)&ADC1->DR;
  DMA_InitStructure.DMA_MemoryBaseAddr = (uint32_t)&jodo[0];
  DMA_InitStructure.DMA_DIR = DMA_DIR_PeripheralSRC;
  DMA_InitStructure.DMA_BufferSize = sizeof(uint32_t);
  DMA_InitStructure.DMA_PeripheralInc = DMA_PeripheralInc_Disable;
  DMA_InitStructure.DMA_MemoryInc = DMA_PeripheralInc_Disable;
  DMA_InitStructure.DMA_PeripheralDataSize = DMA_PeripheralDataSize_Word;
  DMA_InitStructure.DMA_MemoryDataSize = DMA_MemoryDataSize_Word;
  DMA_InitStructure.DMA_Mode = DMA_Mode_Circular;
  DMA_InitStructure.DMA_Priority = DMA_Priority_High;
  DMA_InitStructure.DMA_M2M = DMA_M2M_Disable;
  DMA_Init(DMA1_Channel1, &DMA_InitStructure);
  DMA_Cmd(DMA1_Channel1, ENABLE);
}

void Delay(void) {
   int i;

   for (i = 0; i < 500000; i++) {}
}

int main() {
  // LCD 관련 설정은 LCD_Init에 구현되어 있으므로 여기서 할 필요 없음
  SystemInit();
  RCC_Configure();
  GPIO_Configure();
  ADC_Configure();
  DMA_Configure();
          
  
  LCD_Init();

  // ------------------------------------

  
  LCD_Clear(WHITE);
  LCD_ShowString(25, 100, "MON_Team03", BLACK, WHITE);
  
  int grayBackgroundFlag = 0;
  int background = WHITE;
  int font = BLACK;
  int threshold=3800;
  while(1){
    int light = jodo[0];
    if (light > threshold && grayBackgroundFlag == 0) {
      grayBackgroundFlag = 1;
      background = WHITE;
      font = BLACK;
      LCD_Clear(background);
    }
    if (light < threshold && grayBackgroundFlag == 1) {
      grayBackgroundFlag = 0;
      background = GRAY;
      font = WHITE;
      LCD_Clear(background);
    }
    
    LCD_ShowString(25, 100, "Mon_Team03", font, background);
    
    LCD_ShowNum(65, 160, light, 4, font, background);
    Delay();
  }
}