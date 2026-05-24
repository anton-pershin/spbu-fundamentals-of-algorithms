import time
import random
import numpy as np

# Импортируем классы из модулей
from huffman import HuffmanCoding
from huffman_node import HuffmanNode
from huffman_hybrid import HuffmanHybrid

import os
from pathlib import Path

script_dir = Path(__file__).parent
os.chdir(script_dir)


def test_huffman(huffman_class, sequence, iterations=5):
    total_encode = 0.0
    total_decode = 0.0
    
    for _ in range(iterations):
        h = huffman_class()
        
        # Измеряем encode
        start = time.perf_counter()
        bits = h.encode(sequence)
        end = time.perf_counter()
        total_encode += (end - start)
        
        # Измеряем decode
        start = time.perf_counter()
        decoded = h.decode(bits)
        end = time.perf_counter()
        total_decode += (end - start)
        
        # Проверяем корректность
        assert decoded == sequence, f"Ошибка: декодирование не совпало для {huffman_class.__name__}"
    
    return total_encode / iterations, total_decode / iterations


def run_benchmark():
    """Запускает бенчмарк для всех реализаций и размеров"""
    
    test_sizes = [100, 1000, 10000, 50000]
    results = []
    
    # Три реализации
    implementations = [
        ("List", HuffmanCoding),
        ("Node", HuffmanNode),
        ("Hybrid", HuffmanHybrid)
    ]
    
    print("=" * 70)
    print("Бенчмарк Huffman Coding")
    print("=" * 70)
    print()
    
    for size in test_sizes:
        print(f"Размер последовательности: {size}")
        print("-" * 40)
        
        # Генерируем случайную последовательность (байты 0-255)
        sequence = [random.randint(0, 255) for _ in range(size)]
        
        for name, cls in implementations:
            enc_time, dec_time = test_huffman(cls, sequence, iterations=3)
            results.append((name, size, enc_time, dec_time))
            print(f"  {name:20} Encode: {enc_time*1000:8.3f} ms, Decode: {dec_time*1000:8.3f} ms")
        
        print()
    
    # Финальная таблица
    print("=" * 70)
    print("Сводная таблица (время в миллисекундах)")
    print("=" * 70)
    print(f"{'Method':<20} {'Size':<10} {'Encode (ms)':<12} {'Decode (ms)':<12}")
    print("-" * 60)
    
    for name, size, enc, dec in results:
        print(f"{name:<20} {size:<10} {enc*1000:<12.3f} {dec*1000:<12.3f}")


def test_correctness():
    """Проверяет корректность всех реализаций на маленьких примерах"""
    
    print("=" * 70)
    print("Тест корректности")
    print("=" * 70)
    
    test_cases = [
        ([], "пустая последовательность"),
        ([1], "один символ"),
        ([1, 2, 3, 4, 5], "уникальные символы"),
        ([1, 1, 1, 2, 2, 3], "повторяющиеся символы"),
        (list("abracadabra"), "строка"),
        ([random.randint(0, 10) for _ in range(100)], "случайная")
    ]
    
    implementations = [
        ("HuffmanCoding (List)", HuffmanCoding),
        ("HuffmanNode", HuffmanNode),
        ("HuffmanHybrid", HuffmanHybrid),
    ]
    
    for name, cls in implementations:
        print(f"\n{name}:")
        all_passed = True
        
        for seq, desc in test_cases:
            h = cls()
            bits = h.encode(seq)
            decoded = h.decode(bits)
            
            if decoded == seq:
                print(f"  ✅ {desc}")
            else:
                print(f"  ❌ {desc}")
                all_passed = False
        
        if all_passed:
            print(f"  ✅ Все тесты пройдены!")
        else:
            print(f"  ❌ Есть ошибки!")

def compare_with_lossy():
    """Сравнение с LossyCompression (на реальных данных)"""
    print("\n" + "=" * 70)
    print("Тест LossyCompression (с реальными данными)")
    print("=" * 70)
    
    # Получаем путь к файлу
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "ts_homework_practicum_5.txt")
    
    if not os.path.exists(file_path):
        print(f"Файл не найден: {file_path}")
        print(f"Текущая директория: {os.getcwd()}")
        return
    
    try:
        from huffman import LossyCompression
        
        # Загружаем данные
        ts = np.loadtxt(file_path)
        print(f"Размер исходных данных: {len(ts)} значений")
        print(f"Диапазон значений: [{ts.min():.2f}, {ts.max():.2f}]")
        
        # Тестируем LossyCompression с разными параметрами
        deltas = [0.01, 0.05, 0.1, 0.5]
        bits_per_samples = [4, 6, 8, 10]
        
        print("\nРезультаты сжатия:")
        print("-" * 70)
        print(f"{'delta':<10} {'bits/sample':<12} {'Compression ratio':<18} {'RMSE':<12}")
        print("-" * 70)
        
        best_ratio = 0
        best_rmse = float('inf')
        best_params = None
        
        for delta in deltas:
            for bps in bits_per_samples:
                compressor = LossyCompression(delta=delta, bits_per_sample=bps)
                
                # Сжатие
                bits = compressor.compress(ts)
                
                # Восстановление
                decompressed = compressor.decompress(bits)
                
                # Метрики
                ratio = (len(ts) * 32 * 8) / len(bits)  # исходные 32-битные float
                rmse = np.sqrt(np.mean((ts - decompressed) ** 2))
                
                print(f"{delta:<10} {bps:<12} {ratio:<18.2f} {rmse:<12.6f}")
                
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_rmse = rmse
                    best_params = (delta, bps)
        
        print("-" * 70)
        print(f"\nЛучший результат: delta={best_params[0]}, bits_per_sample={best_params[1]}")
        print(f"  Коэффициент сжатия: {best_ratio:.2f}")
        print(f"  Ошибка восстановления (RMSE): {best_rmse:.6f}")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()

def compare_all_lossy():
    """Сравнивает LossyCompression из всех реализаций"""
    print("\n" + "=" * 70)
    print("Сравнение LossyCompression из разных реализаций")
    print("=" * 70)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "ts_homework_practicum_5.txt")
    
    if not os.path.exists(file_path):
        print(f"Файл не найден: {file_path}")
        return
    
    ts = np.loadtxt(file_path)
    
    implementations = [
        ("List (huffman.py)", "huffman"),
        ("Node (huffman_node.py)", "huffman_node"),
        ("Hybrid (huffman_hybrid.py)", "huffman_hybrid")
    ]
    
    delta = 0.01
    bits_per_sample = 8
    
    print(f"\nПараметры: delta={delta}, bits_per_sample={bits_per_sample}")
    print("-" * 70)
    print(f"{'Implementation':<25} {'Bits length':<12} {'Ratio':<10} {'Time (ms)':<10}")
    print("-" * 70)
    
    for name, module_name in implementations:
        try:
            module = __import__(module_name)
            LossyClass = module.LossyCompression
            
            compressor = LossyClass(delta=delta, bits_per_sample=bits_per_sample)
            
            start = time.perf_counter()
            bits = compressor.compress(ts)
            compress_time = (time.perf_counter() - start) * 1000
            
            ratio = (len(ts) * 32 * 8) / len(bits)
            
            print(f"{name:<25} {len(bits):<12} {ratio:<10.2f} {compress_time:<10.3f}")
            
        except Exception as e:
            print(f"{name:<25} {'ERROR':<12} {'-':<10} {str(e)[:30]}")


if __name__ == "__main__":
    # 1. Проверяем корректность
    test_correctness()
    
    print("\n")
    
    # 2. Запускаем бенчмарк
    run_benchmark()
    
    # 3. Тестируем LossyCompression
    compare_with_lossy()

    compare_all_lossy()