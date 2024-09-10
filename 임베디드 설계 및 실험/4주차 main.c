#include "stm32f10x.h"

#define RCC_APB2_ENR *(volatile unsigned int *) 0x40021018

#define GPIOA_CRL *(volatile unsigned int *) 0x40010800
#define GPIOB_CRH *(volatile unsigned int *) 0x40010C04
#define GPIOC_CRH *(volatile unsigned int *) 0x40011004
#define GPIOC_CRL *(volatile unsigned int *) 0x40011000
// #define GPIOD_CRL *(volatile unsigned int *) 0x40011400

#define GPIOE_CRL *(volatile unsigned int *) 0x40011800
#define GPIOE_BSRR *(volatile unsigned int *) 0x40011810

#define GPIOA_IDR *(volatile unsigned int *) 0x40010808
#define GPIOB_IDR *(volatile unsigned int *) 0x40010C08
#define GPIOC_IDR *(volatile unsigned int *) 0x40011008

#define RESET 0x44444444

void delay(){
  int i;
  for(i=0;i<10000000;i++){}
}

int main(void){
  RCC_APB2_ENR = 0x007C;
 
  GPIOA_CRL &= 0x44444440;
  GPIOA_CRL |= 0x00000008;
 
  GPIOB_CRH &= 0x44444044;
  GPIOB_CRH |= 0x00000800;
 
  GPIOC_CRH &= 0x44044444;
  GPIOC_CRH |= 0x00800000;
 
  GPIOC_CRL &= 0x44404444;
  GPIOC_CRL |= 0x00080000;
 
  GPIOE_CRL &= 0x44444400;
  GPIOE_CRL |= 0x00000033;

  unsigned int KEY1 = 0x0010;
  unsigned int KEY2 = 0x0400;
  unsigned int KEY3 = 0x2000;
  unsigned int KEY4 = 0x0001;

  GPIOE_BSRR |= 0x00000003;

  while(1)
  {
   
    if((~GPIOC_IDR & KEY1)) //정방향 회전
    {
      GPIOE_BSRR |= 0x00020001;
    }
    else if((~GPIOB_IDR & KEY2)) //역방향 회전
    {
      GPIOE_BSRR |= 0x00010002;
    }
    else if((~GPIOC_IDR & KEY3)) //정방향2초 역방향2초
    {
      GPIOE_BSRR |= 0x00020001;
      delay();
      GPIOE_BSRR |= 0x00010002;
      delay();
      GPIOE_BSRR |= 0x00000003;
    }
    else if((~GPIOA_IDR & KEY4)) //정지
    {
      GPIOE_BSRR  |= 0x00000003;
    }
  }

  return 0;
}