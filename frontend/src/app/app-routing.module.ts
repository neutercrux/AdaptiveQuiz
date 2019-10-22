import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { SubjectComponent } from './subject/subject.component';
import { QuestionComponent } from './question/question.component';
import { NotFoundComponent } from './not-found/not-found.component';

const routes: Routes = [
  { path: '' , redirectTo: '/subject', pathMatch:'full' },
  { path: 'subject' , component: SubjectComponent },
  { path: 'subject/:name' , component: QuestionComponent },
  { path: "**", component: NotFoundComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
export const RoutingComponents = [ SubjectComponent, QuestionComponent, NotFoundComponent] 