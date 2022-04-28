# Backend Homework Assignment

Философия кода
----------------------------
В Recar мы стремимся писать чистый и простой код, снабженный модульными тестами и простой в сопровождении. Мы также придаем большое значение последовательности. Мы ожидаем увидеть те же ценности, что и в решении задачи.

Требования
----------------------------
* Мы рекомендуем выбрать ваш любимый язык программирования. Здесь нет никаких ограничений. Мы хотим, чтобы вы показали нам, на что вы способны с помощью инструментов, которые вы уже хорошо знаете.
* Ваше решение должно соответствовать философии, описанной выше.
* Использование дополнительных библиотек (нестандартных) запрещено. Это ограничение не применяется для модульных тестов и сборки.
* Должен быть простой способ запустить решение и тесты. (в случае с python это может быть что-то вроде: "make main", "pytest tests.py").
* Краткая документация проектных решений и предположений может быть представлена в самом коде.
* Убедитесь, что ваши входные данные загружены из файла (по умолчанию предполагается имя 'input.txt')
* Убедитесь, что ваше решение выводит данные в файл output.txt в формате, описанном ниже
* Ваш дизайн должен быть достаточно гибким, чтобы позволить легко добавлять новые правила и изменять существующие.


Проблема
----------------------------
Когда что-то покупается, это должно быть отправлено, доступны различные варианты доставки. 
Каждый предмет, в зависимости от его размера, получает соответствующий размер упаковки:

  * S - Small
  * M - Medium 
  * L - Large 

Стоимость доставки зависит от размера пакета и поставщика:

| Provider | Package Size | Price  |
|---|---|---|
| SimoSiuntos| S| 1.50 € |
| SimoSiuntos| M| 4.90 € |
| SimoSiuntos| L| 6.90 € |
| JonasShipping| S| 2 €|
| JonasShipping| M| 3 €|
| JonasShipping| L| 4 €|


**Ваша задача - создать модуль расчета скидки на отгрузку.**

Во-первых, вы должны внедрить такие правила:
  * Все S-отправки всегда должны соответствовать самой низкой цене S-пакета среди поставщиков.
  * Третья отправка L через SimoSiuntos должна быть бесплатной, но только один раз в календарный месяц.
  * Накопленные скидки не могут превышать 10 € в течение календарного месяца. Если средств недостаточно для полного
  для полного покрытия скидки в этом календарном месяце, она должна быть покрыта частично.

**Ваш дизайн должен быть достаточно гибким, чтобы можно было легко добавлять новые правила и изменять существующие.**

Транзакции участника перечисляются в файле 'input.txt', каждая строка которого содержит: дату (без часов, в формате ISO), код размера упаковки и код перевозчика, разделенные пробелами:
```
2015-02-01 S JonasShipping
2015-02-02 S JonasShipping
2015-02-03 L SimoSiuntos
2015-02-05 S SimoSiuntos
2015-02-06 S JonasShipping
2015-02-06 L SimoSiuntos
2015-02-07 L JonasShipping
2015-02-08 M JonasShipping
2015-02-09 L SimoSiuntos
2015-02-10 L SimoSiuntos
2015-02-10 S JonasShipping
2015-02-10 S JonasShipping
2015-02-11 L SimoSiuntos
2015-02-12 M JonasShipping
2015-02-13 M SimoSiuntos
2015-02-15 S JonasShipping
2015-02-17 L SimoSiuntos
2015-02-17 S JonasShipping
2015-02-24 L SimoSiuntos
2015-02-29 CUSPS
2015-03-01 S JonasShipping
```
Ваша программа должна выводить транзакции и добавлять сниженную цену отгрузки и скидку на отгрузку (или '-', если ее нет). Программа должна добавлять слово 'Ignored', если формат строки неправильный или перевозчик/размеры не распознаны.
```
2015-02-01 S JonasShipping 1.50 0.50
2015-02-02 S JonasShipping 1.50 0.50
2015-02-03 L SimoSiuntos 6.90 -
2015-02-05 S SimoSiuntos 1.50 -
2015-02-06 S JonasShipping 1.50 0.50
2015-02-06 L SimoSiuntos 6.90 -
2015-02-07 L JonasShipping 4.00 -
2015-02-08 M JonasShipping 3.00 -
2015-02-09 L SimoSiuntos 0.00 6.90
2015-02-10 L SimoSiuntos 6.90 -
2015-02-10 S JonasShipping 1.50 0.50
2015-02-10 S JonasShipping 1.50 0.50
2015-02-11 L SimoSiuntos 6.90 -
2015-02-12 M JonasShipping 3.00 -
2015-02-13 M SimoSiuntos 4.90 -
2015-02-15 S JonasShipping 1.50 0.50
2015-02-17 L SimoSiuntos 6.90 -
2015-02-17 S JonasShipping 1.90 0.10
2015-02-24 L SimoSiuntos 6.90 -
2015-02-29 CUSPS Ignored
2015-03-01 S JonasShipping 1.50 0.50
```

Критерии оценки
----------------------------
* Ваше решение будет оцениваться по тому, насколько хорошо реализованы все требования.