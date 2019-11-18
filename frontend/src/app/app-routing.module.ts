import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { SubjectComponent } from './subject/subject.component';
import { QuestionComponent } from './question/question.component';
import { NotFoundComponent } from './not-found/not-found.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { ResultsComponent } from './results/results.component';

const routes: Routes = [
  { path: '' , component: LoginComponent},
  { path: 'login' , component: LoginComponent},
  { path: 'register' , component: RegisterComponent},
  { path: 'subject' , component: SubjectComponent },
  { path: 'subject/:name' , component: QuestionComponent },
  { path: 'results/:name' , component: ResultsComponent },
  { path: "**", component: NotFoundComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
export const RoutingComponents = [ SubjectComponent, QuestionComponent, NotFoundComponent] 