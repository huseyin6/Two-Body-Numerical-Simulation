#include<stdio.h>
#include<stdlib.h>
#include<math.h>

#define TRUE 1
#define FALSE 0

#define N 4

struct TwoBodyModel{
	
	double m1;
	double m2;
	double m1_2;
	double u[N];
	double dimension[N];
	struct	TwoBodyModel *next;	


};

typedef struct TwoBodyModel *body;

struct TwoBodyControl{
	
	double T;
	double q;
	double e;
	double h;
		
		struct	TwoBodyControl *next;	

};

typedef struct TwoBodyController *controller;

void init(struct TwoBodyModel *body, struct TwoBodyControl *controller);
double *derivative(struct TwoBodyModel *body, struct TwoBodyControl *controller);
void RK4(struct TwoBodyModel *body, struct TwoBodyControl *controller);
void euler(struct TwoBodyModel *body, struct TwoBodyControl *controller);
void apply(struct TwoBodyModel *body, struct TwoBodyControl *controller);
void calnewdimension(struct TwoBodyModel *body);
void calculation_RK4(struct TwoBodyModel *body, struct TwoBodyControl *controller);
void calculation_euler(struct TwoBodyModel *body, struct TwoBodyControl *controller);


int main(){

    struct TwoBodyModel body;
    struct TwoBodyControl controller;
    apply(&body, &controller);
   
	return 0;
	
}

void init(struct TwoBodyModel *body, struct TwoBodyControl *controller){
	
	
	body->m1 = 1;
	body->m2 = 1*controller->q;
	body->m1_2 = body->m1+body->m2;
	body->dimension[0] = 0, body->dimension[1] = 0, body->dimension[2] = 0, body->dimension[3] = 0;
	body->u[0] = 1, body->u[1] = 0,  body->u[2] = 0,  body->u[3] = sqrt((1 + controller->q) * (1 + controller->e));   
	
	

}

double *derivative(struct TwoBodyModel *body, struct TwoBodyControl *con){
	float *du;
	double *r, distanceR;
	int i=0;
	du=(float*) malloc(4*sizeof(float));
	r=(double*) malloc(4*sizeof(double));
	r[0]=body->u[0];
	r[1]=body->u[1];
	distanceR = sqrt(pow(r[0], 2) + pow(r[1], 2));	

	
	for(i = 0; i < 2; i++){
		du[i] = body->u[i + 2];
        du[i + 2] = -((1 + con->q) * r[i] ) / pow(distanceR, 3);
	} 

	return du;
	
}

void RK4(struct TwoBodyModel *body, struct TwoBodyControl *controller){
	
	float *du;
	int i,j;
	
	du=(float*) malloc(4*sizeof(float));
	int len=sizeof(body->u) / sizeof(body->u[0]);
	
	double a[4] = { controller->h/2, controller->h/2, controller->h, 0 };
    double b[4] = {controller->h/6, controller->h/3, controller->h/3, controller->h/6};
    
    double u0[4]= {0,0,0,0};
    double ut[4] = {0,0,0,0};
    
    for(i = 0 ; i < len; i++){
        u0[i] = body->u[i];
        ut[i] = 0;
      }  
     for(j = 0; j<4; j++){
            du = derivative(body, controller);
            for(int i=0; i<len; i++){
                body->u[i] = u0[i] + a[j]*du[i];
                ut[i] = ut[i] + b[j]*du[i];
                
}  
}
        for (i = 0; i < len; i++){

            body->u[i] = u0[i] + ut[i];
            
	}
}

void calculation_RK4(struct TwoBodyModel *body, struct TwoBodyControl *controller) {
	
	float *du;
    int i;
    
    FILE *fptr;
	fptr=fopen("Project_LocationVector.txt", "w");
    
	for( i = 0; i<(controller->T)/(controller->h); i++){
		RK4(body, controller);
		
	calnewdimension(body);
	fprintf(fptr, "%lf", body->dimension[0]);
	fprintf(fptr, ", %lf", body->dimension[1]);
	fprintf(fptr, ", %lf", body->dimension[2]);
	fprintf(fptr, ", %lf\n", body->dimension[3]);
		
	}
	
}


void euler(struct TwoBodyModel *body, struct TwoBodyControl *controller){
	
    float *du;
    int i;
    
    du = derivative(body,controller);
    
        for(i=0; i < 4; i++){
		
            body->u[i] = body->u[i] + controller->h * du[i];
}
}

void calculation_euler(struct TwoBodyModel *body, struct TwoBodyControl *controller) {
	
	float *du;
    int i;
    FILE *fptr;
	fptr = fopen("Project_LocationVector.txt", "w");
	
	for( i = 0; i<(controller->T) / (controller->h); i++){
		euler(body, controller);
		
	calnewdimension(body);
	fprintf(fptr, "%lf", body->dimension[0]);
	fprintf(fptr, ", %lf", body->dimension[1]);
	fprintf(fptr, ", %lf", body->dimension[2]);
	fprintf(fptr, ", %lf\n", body->dimension[3]);
		
	}	
}


void calnewdimension(struct TwoBodyModel *body){
	
	double r = 1;
	double a1 = (body->m2 / body->m1_2) * r;   
	double a2 = (body->m1 / body->m1_2) * r;
	
	body->dimension[0] = - a2 * body->u[0];
    body->dimension[1] = - a2 * body->u[1];
    body->dimension[2] = a1 * body->u[0];
    body->dimension[3] = a1 * body->u[1];

}


void apply(struct TwoBodyModel *body, struct TwoBodyControl *controller){
	
 	int choice;
 	int i;
   	FILE *fptr;
	fptr=fopen("Project_LocationVector.txt", "w");
	   
    printf("Enter Mass ratio: ");
    scanf("%lf", &controller->q);
    printf("Enter Eccentricity: ");
    scanf("%lf", &controller->e);
    printf("Enter T: ");
    scanf("%lf", &controller->T);
    printf("Enter Step-size: ");
    scanf("%lf", &controller->h);
    init(body, controller);
    
    printf("Choose method\n1:RungeKutta\n2:Euler\n");
    scanf("%d", &choice);
    

    
    switch(choice) {
    	
    	case 1:
    		calculation_RK4(body, controller);
    		break;
    	case 2:
    		calculation_euler(body, controller);
    		break;
    	default:
    		printf("Wrong Choose!");
    		exit(0);
    		break;
	}
       				
	
}


