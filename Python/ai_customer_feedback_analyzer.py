"""Analyze customer review sentiment with VADER (lexicon-based NLP)."""
import csv
from pathlib import Path
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

REVIEWS_FILE = Path(__file__).with_name('sample_reviews.csv')


def classify(score):
    if score >= 0.05:
        return 'Positive'
    if score <= -0.05:
        return 'Negative'
    return 'Neutral'


def main():
    if not REVIEWS_FILE.exists():
        with REVIEWS_FILE.open('w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['review'])
            writer.writerows([
                ['Amazing service and very friendly staff!'],
                ['The delivery was late and the product was broken.'],
                ['The store opens at 9 AM.'],
                ['I love how easy this app is to use.'],
                ['Very disappointing experience.'],
            ])
        print(f'Created sample dataset: {REVIEWS_FILE.name}')

    analyzer = SentimentIntensityAnalyzer()
    counts = {'Positive': 0, 'Negative': 0, 'Neutral': 0}
    with REVIEWS_FILE.open(newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames or 'review' not in reader.fieldnames:
            raise ValueError('CSV needs a review column')
        for row in reader:
            review = row['review'].strip()
            if not review:
                continue
            score = analyzer.polarity_scores(review)['compound']
            label = classify(score)
            counts[label] += 1
            print(f'[{label:8}] ({score:+.3f}) {review}')

    print('\n=== SENTIMENT SUMMARY ===')
    for label, count in counts.items():
        print(f'{label}: {count}')
    print('\nNote: Lexicon-based sentiment can misread sarcasm and context.')


if __name__ == '__main__':
    main()
