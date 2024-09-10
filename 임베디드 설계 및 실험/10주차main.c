#include "misc.h"
#include "stm32f10x.h"
#include "stm32f10x_gpio.h"
#include "stm32f10x_rcc.h"
#include "stm32f10x_usart.h"
#include "stm32f10x.h"
#include "core_cm3.h"
#include "stm32f10x_exti.h"
#include "lcd.h"
#include "touch.h"
#include "stm32f10x_adc.h"

int color[12] ={WHITE,CYAN,BLUE,RED,MAGENTA,LGRAY,GREEN,YELLOW,BROWN,BRRED,GRAY};
uint16_t sensor_value = 0; 
uint16_t x = 0, y = 0;
uint16_t px = 0, py = 0;

GPIO_InitTypeDef GPIO_init;             
USART_InitTypeDef USART_InitStructure;       
NVIC_InitTypeDef NVIC_init;                    
 
void RCC_Configuration(void){    
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB, ENABLE);     
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_ADC1, ENABLE);     
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_AFIO, ENABLE);
}           
 
void GPIO_Configuration(void){
    GPIO_init.GPIO_Pin = GPIO_Pin_0;  
    GPIO_init.GPIO_Mode = GPIO_Mode_AIN;    
    GPIO_Init(GPIOB, &GPIO_init);        
}
 
void NVIC_Configuration(void){           

    NVIC_PriorityGroupConfig(NVIC_PriorityGroup_0);
    NVIC_EnableIRQ(ADC1_2_IRQn);
  
    NVIC_init.NVIC_IRQChannel = ADC1_2_IRQn;         
    NVIC_init.NVIC_IRQChannelPreemptionPriority = 0; 
    NVIC_init.NVIC_IRQChannelSubPriority = 0;        
    NVIC_init.NVIC_IRQChannelCmd = ENABLE;              
    NVIC_Init(&NVIC_init); 
}

void ADC_Configuration(){
    ADC_DeInit(ADC1);
     ADC_InitTypeDef ADC_InitStructure;
    ADC_InitStructure.ADC_Mode = ADC_Mode_Independent;
    ADC_InitStructure.ADC_ScanConvMode = DISABLE;
    ADC_InitStructure.ADC_ContinuousConvMode = ENABLE;
    ADC_InitStructure.ADC_ExternalTrigConv = ADC_ExternalTrigConv_None;
    ADC_InitStructure.ADC_DataAlign = ADC_DataAlign_Right;
    ADC_InitStructure.ADC_NbrOfChannel = 1;
    ADC_Init(ADC1, &ADC_InitStructure);
   
    ADC_RegularChannelConfig(ADC1, ADC_Channel_8, 1, ADC_SampleTime_239Cycles5);    
    ADC_ITConfig(ADC1, ADC_IT_EOC, ENABLE);
    ADC_Cmd(ADC1, ENABLE);
    ADC_ResetCalibration(ADC1);
    while(ADC_GetResetCalibrationStatus(ADC1));
    ADC_StartCalibration(ADC1);
    while(ADC_GetCalibrationStatus(ADC1));
    ADC_SoftwareStartConvCmd(ADC1, ENABLE);
}
 

void ADC1_2_IRQHandler(void) {
    if (ADC_GetITStatus(ADC1, ADC_IT_EOC) != RESET) {
      sensor_value = ADC_GetConversionValue(ADC1);
      ADC_ClearITPendingBit(ADC1, ADC_IT_EOC);   
   }    
}

int main(void){
    SystemInit();        
 
    RCC_Configuration();        
    GPIO_Configuration();        
    ADC_Configuration();
    NVIC_Configuration();        
    
    LCD_Init();
    Touch_Configuration();
    Touch_Adjust();
    LCD_Clear(WHITE);
    
   while(1){
      LCD_ShowString(0, 0, "MON_Team03", BLACK, WHITE);
      Touch_GetXY(&x, &y, 1);
      Convert_Pos(x, y, &px, &py);
      LCD_ShowNum(0, 100, sensor_value, 4 , BLACK, WHITE);
      LCD_ShowNum(0, 50, px, 4, BLACK, WHITE);
      LCD_ShowNum(0, 70, py, 4, BLACK, WHITE);
      LCD_DrawCircle(px, py, 10);
   }
}