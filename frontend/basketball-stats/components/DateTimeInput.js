import React, { useState, useEffect } from 'react';
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import styles from '../styles/DateTimeInput.module.css';

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
        placeholderText={placeholder || "MM/DD/YYYY HH:MM"}
        className={styles.dateTimeInput}
      />
    </div>
  );
};

export default DateTimeInput;

