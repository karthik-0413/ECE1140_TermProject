import test1, test2

def handle_test_signal(value):
    print("Received signal with value: ", value)

if __name__ == "__main__":
    # Run test2 file
    test2.test2.emit(1)
    test1.test1.connect(handle_test_signal)