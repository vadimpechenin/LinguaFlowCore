"""
Генерирует 4 типа заданий.
Прямая карточка (Flashcard): На экране слово на иностранном языке — вы должны вспомнить перевод.
Обратная карточка: На экране слово на родном языке — нужно воспроизвести иностранный оригинал (это сложнее и эффективнее).
Множественный выбор (Multiple Choice): Выбор правильного перевода из 4–5 предложенных вариантов.
Сборка слова из букв / Скрембл: Тренирует правописание, заставляя расставить буквы в нужном порядке.
"""
import random


class ExamGenerator:

   def generate(self, words, size: int):

       selected = random.sample(words, min(size, len(words)))
       questions = []

       for w in selected:

           task_type = random.choice([
               "flashcard_forward",
               "flashcard_reverse",
               "multiple_choice",
               "scramble"
           ])

           if task_type == "flashcard_forward":
               questions.append({
                   "word_id": w.id,
                   "type": task_type,
                   "question": f"Translate: {w.texten}",
                               "options": None
               })

           elif task_type == "flashcard_reverse":
               questions.append({
                   "word_id": w.id,
                   "type": task_type,
                   "question": f"Translate: {w.textl}",
                               "options": None
               })

           elif task_type == "multiple_choice":
               options = self._generate_options(w, words)
               questions.append({
                   "word_id": w.id,
                   "type": task_type,
                   "question": f"Choose translation for {w.texten}",
                   "options": options
               })

           elif task_type == "scramble":
               scrambled = "".join(random.sample(w.texten, len(w.texten)))
               questions.append({
                   "word_id": w.id,
                   "type": task_type,
                   "question": f"Unscramble: {scrambled}",
                               "options": [w.texten]
               })

       return questions

   def _generate_options(self, correct_word, all_words):
       distractors = random.sample(
           [w.textl for w in all_words if w.id != correct_word.id],
           3
       )
       options = distractors + [correct_word.textl]
       random.shuffle(options)
       return options
