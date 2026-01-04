/* Seat Selection JavaScript */

document.addEventListener('DOMContentLoaded', function() {
    const selectedSeats = new Set();
    const seatMap = document.getElementById('seatMap');
    const selectionCard = document.getElementById('selectionCard');
    const selectedSeatsDisplay = document.getElementById('selectedSeatsDisplay');
    const totalSeatsSpan = document.getElementById('totalSeats');
    const seatsInput = document.getElementById('seatsInput');
    const bookBtn = document.getElementById('bookBtn');
    const loginBtn = document.getElementById('loginBtn');
    const signupBtn = document.getElementById('signupBtn');
    
    function updateDisplay() {
        const seatsArray = Array.from(selectedSeats).sort((a, b) => {
            const rowA = a.charAt(0);
            const rowB = b.charAt(0);
            const numA = parseInt(a.slice(1));
            const numB = parseInt(b.slice(1));
            
            if (rowA !== rowB) return rowA.localeCompare(rowB);
            return numA - numB;
        });
        
        if (seatsArray.length > 0) {
            selectionCard.style.display = 'block';
            selectedSeatsDisplay.innerHTML = seatsArray.map(seat => 
                `<span class="badge bg-success fs-6 px-3 py-2">${seat}</span>`
            ).join('');
            totalSeatsSpan.textContent = seatsArray.length;
            seatsInput.value = seatsArray.join(',');
            
            if (bookBtn) {
                bookBtn.disabled = false;
            }
            if (loginBtn) {
                loginBtn.style.display = 'inline-block';
            }
            if (signupBtn) {
                signupBtn.style.display = 'inline-block';
            }
        } else {
            selectionCard.style.display = 'none';
            selectedSeatsDisplay.innerHTML = '';
            totalSeatsSpan.textContent = '0';
            seatsInput.value = '';
            
            if (bookBtn) {
                bookBtn.disabled = true;
            }
            if (loginBtn) {
                loginBtn.style.display = 'none';
            }
            if (signupBtn) {
                signupBtn.style.display = 'none';
            }
        }
    }
    
    seatMap.addEventListener('click', function(e) {
        const seat = e.target.closest('.seat');
        
        if (!seat || seat.classList.contains('booked')) return;
        
        const seatId = seat.dataset.seat;
        
        if (seat.classList.contains('selected')) {
            seat.classList.remove('selected');
            seat.classList.add('available');
            selectedSeats.delete(seatId);
        } else {
            seat.classList.remove('available');
            seat.classList.add('selected');
            selectedSeats.add(seatId);
        }
        
        updateDisplay();
    });
    
    const bookingForm = document.getElementById('bookingForm');
    if (bookingForm) {
        bookingForm.addEventListener('submit', function(e) {
            if (selectedSeats.size === 0) {
                e.preventDefault();
                alert('Please select at least one seat before booking.');
                return false;
            }
            
            if (bookBtn) {
                bookBtn.disabled = true;
                bookBtn.innerHTML = '<span class="loading me-2"></span>Processing...';
            }
        });
    }
    
    updateDisplay();
});
