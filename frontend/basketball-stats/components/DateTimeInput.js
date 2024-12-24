import React, { useState, useEffect, forwardRef } from 'react';
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import styles from '../styles/DateTimeInput.module.css';

const CustomInput = forwardRef(({ value, onClick }, ref) => (
  <input
    className={styles.dateTimeInput}
    onClick={onClick}
    ref={ref}
    value={value || '__/__/____ __:__'}
    readOnly
  />
));

const DateTimeInput = ({ value, onChange, placeholder }) => {
  const [selectedDate, setSelectedDate] = useState(value ? new Date(value) : null);

  useEffect(() => {
    setSelectedDate(value ? new Date(value) : null);
  }, [value]);

  const handleChange = (date) => {
    setSelectedDate(date);
    if (date) {
      const formattedDate = date.toLocaleString('en-US', {
        month: '2-digit',
        day: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
      }).replace(',', '');
      onChange(formattedDate);
    } else {
      onChange('');
    }
  };

  const years = Array.from({ length: 50 }, (_, i) => new Date().getFullYear() - 25 + i);
  const months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ];

  return (
    <div className={styles.dateTimeInputWrapper}>
      <DatePicker
        selected={selectedDate}
        onChange={handleChange}
        showTimeSelect
        timeFormat="HH:mm"
        timeIntervals={15}
        timeCaption="Time"
        dateFormat="MM/dd/yyyy HH:mm"
        customInput={<CustomInput />}
        popperClassName={styles.datePickerPopper}
        calendarClassName={styles.datePickerCalendar}
        wrapperClassName={styles.datePickerWrapper}
        dayClassName={() => styles.datePickerDay}
        monthClassName={() => styles.datePickerMonth}
        timeClassName={() => styles.datePickerTime}
        className={styles.datePicker}
        renderCustomHeader={({
          date,
          changeYear,
          changeMonth,
          decreaseMonth,
          increaseMonth,
          prevMonthButtonDisabled,
          nextMonthButtonDisabled,
        }) => (
          <div className={styles.datePickerHeader}>
            <button onClick={decreaseMonth} disabled={prevMonthButtonDisabled}>
              {"<"}
            </button>
            <select
              value={date.getFullYear()}
              onChange={({ target: { value } }) => changeYear(Number(value))}
            >
              {years.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
            <select
              value={months[date.getMonth()]}
              onChange={({ target: { value } }) => changeMonth(months.indexOf(value))}
            >
              {months.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
            <button onClick={increaseMonth} disabled={nextMonthButtonDisabled}>
              {">"}
            </button>
          </div>
        )}
      />
    </div>
  );
};

export default DateTimeInput;

