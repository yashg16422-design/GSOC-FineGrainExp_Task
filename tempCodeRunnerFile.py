if RunMode in ("1", "3"):
        _, t_write = measure_time(
            individual.write,
            records,
            IndividualDir
        )
        print(f"Write time        : {t_write:.4f} seconds")
